import connexion
import json
from connexion import NoContent
import os.path
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from add_orders import AddOrder
from payments import Payment
import datetime
import mysql.connector
import pymysql
import yaml
import logging.config
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
import os

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yaml"
    log_conf_file = "/config/log_conf.yaml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yaml"
    log_conf_file = "log_conf.yaml"

# External Logging Configuration
with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)


with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())
    DB_ENGINE = create_engine(
        f"mysql+pymysql://{app_config['datastore']['user']}:{app_config['datastore']['password']}@{app_config['datastore']['hostname']}:{app_config['datastore']['port']}/{app_config['datastore']['db']}")
    Base.metadata.bind = DB_ENGINE
    DB_SESSION = sessionmaker(bind=DB_ENGINE)

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())


def get_add_order(timestamp):
    """ Gets new order details after the timestamp """
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(
        timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")

    readings = session.query(AddOrder).filter(
        AddOrder.date_created >= timestamp_datetime)

    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())

    session.close()

    logger.info("Query for Order details after %s returns %d results" % (
        timestamp, len(results_list)))

    return results_list, 200


def get_payment(timestamp):
    """ Gets new order details after the timestamp """
    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(
        timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")

    readings = session.query(Payment).filter(
        Payment.date_created >= timestamp_datetime)

    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())

    session.close()

    logger.info("Query for Payment details after %s returns %d results" % (
        timestamp, len(results_list)))

    return results_list, 200


def add_order(body):
    """ Receives a food order """
    session = DB_SESSION()

    forder = AddOrder(body['customer_id'],
                      body['order_id'],
                      body['restaurant'],
                      body['order_total'],
                      body['timestamp'])

    session.add(forder)

    session.commit()
    session.close()

    unique_id_order = body['customer_id']
    logger.debug(
        f"Stored event add_order request with a unique id of {unique_id_order}")

    return NoContent, 201


def payment(body):
    """ Receives a payment """

    session = DB_SESSION()

    pay = Payment(body['customer_id'],
                  body['payment_id'],
                  body['restaurant'],
                  body['timestamp']
                  )

    session.add(pay)

    session.commit()
    session.close()

    unique_id_payment = body['customer_id']
    logger.debug(
        f"Stored event payment request with a unique id of {unique_id_payment}")

    return NoContent, 201


def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (
        app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]

    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).

    consumer = topic.get_simple_consumer(
        consumer_group='event_group', reset_offset_on_start=False, auto_offset_reset=OffsetType.LATEST)

    # This is blocking - it will wait for a new message

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)

        payload = msg["payload"]

        if msg["type"] == "add_order":
            add_order(payload)
        elif msg["type"] == "payment":
            payment(payload)

        # Commit the new message as being read
        consumer.commit_offsets()


app = connexion.FlaskApp(__name__, specification_dir='')

app.add_api("openapi.yaml", base_path="/storage",
            strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    logger.info(
        f"Connecting to DB. Hostname:{app_config['datastore']['hostname']}, Port:{app_config['datastore']['port']}")
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
