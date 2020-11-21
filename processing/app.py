import connexion
import json
from connexion import NoContent
import os.path
import requests
import yaml
import logging.config
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask_cors import CORS, cross_origin
import os


if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yaml"
    log_conf_file = "/config/log_conf.yaml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yaml"
    log_conf_file = "log_conf.yaml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

# External Logging Configuration
with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

url = app_config["eventstore"]["url"]
json_file = app_config["datastore"]["filename"]
time_interval = app_config['scheduler']['period_sec']


def get_stats():

    logger.info("Your request has started")
    if os.path.isfile(json_file):
        with open(json_file, 'r') as file:
            data = json.loads(file.read())
            logger.debug(f"Current Statistics: {data}")
            logger.info("Your request has completed")
        return data, 200
    else:
        logger.error("No data.json exist")
        return "Statistics do not exist", 404


def populate_stats():
    """ Periodically update stats """
    logger.info("Start Periodic Processing")
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if os.path.isfile(json_file):
        with open(json_file, 'r') as file:
            data = json.loads(file.read())
            last_datetime = data["timestamp"]
            data["timestamp"] = now
            # Order Query
            url_order = url + "/orders/add_foods?timestamp=" + last_datetime
            url_payment = url + "/orders/payments?timestamp=" + last_datetime
            try:
                r_order = requests.get(url_order)
                order_data = r_order.json()
                num_order = (len(order_data)) + data["num_order"]
                if num_order != 0:
                    order_total_list = [i["order_total"] for i in order_data]
                    sum_order_total = sum(
                        order_total_list) + data["sum_order_total"]
                    avg_order_total = sum_order_total / num_order
                    data["sum_order_total"] = round(sum_order_total, 2)
                    data["avg_order_total"] = round(avg_order_total, 2)
                    data["num_order"] = num_order
                logger.info(
                    f"Returned number of order events {data['num_order']}")
                # Payment Query
                r2_payment = requests.get(url_payment)
                num_payment = (len(r2_payment.json())) + data["num_payment"]
                if num_payment != 0:
                    data["num_payment"] = num_payment
                logger.info(
                    f"Returned number of payment events {data['num_payment']}")
                with open(json_file, 'w') as file:
                    json_data = json.dumps(data)
                    file.write(json_data)
                logger.debug(f"Current Statistics: {data}")
            except requests.exceptions.RequestException as e:
                logger.error(e)
    else:
        with open(json_file, 'w') as file:
            default_data = {"timestamp": now, "num_order": 0, "num_payment": 0,
                            "sum_order_total": 0, "avg_order_total": 0}
            json_data = json.dumps(default_data)
            file.write(json_data)
        logger.debug(f"Current Statistics: {default_data}")

    logger.info("Start Periodic has ended")


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval',
                  seconds=time_interval)
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

app.add_api("openapi.yaml", base_path="/processing",
            strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100)
