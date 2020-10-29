import connexion
import json
from connexion import NoContent
from pykafka import KafkaClient
import logging.config
import yaml


with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())


with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def get_add_order(index):
    """ Get Order Report in History """
    hostname = "%s:%d" % (
        app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]
    consumer = topic.get_simple_consumer(
        reset_offset_on_start=True, consumer_timeout_ms=600)

    logger.info("Retrieving order report at index %d" % index)
    count = 0
    order = None
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == "add_order":
            if count == index:
                order = msg["payload"]
                return order, 200
            count += 1

    logger.error("Could not find order report at index %d" % index)
    return {"message": "Not Found"}, 404


def get_payment(index):
    """ Get Payment Report in History """
    hostname = "%s:%d" % (
        app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]

    consumer = topic.get_simple_consumer(
        reset_offset_on_start=True, consumer_timeout_ms=600)
    logger.info("Retrieving payment report at index %d" % index)

    count = 0
    payment = None
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == "payment":
            if count == index:
                payment = msg["payload"]
                return payment, 200
            count += 1

        # Find the event at the index you want and
        # return code 200
        # i.e., return event, 200

    logger.error("Could not find payment report at index %d" % index)
    return {"message": "Not Found"}, 404


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    app.run(port=8110)
