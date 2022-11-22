import connexion 
import requests
from connexion import NoContent 
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import yaml
import logging
import logging.config
import json
import os
from flask_cors import CORS, cross_origin

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
  print("In Test Environment")
  app_conf_file = "/config/app_conf.yaml"
  log_conf_file = "/config/log_conf.yaml"
else:
  print("In Dev Environment")
  app_conf_file = "app_conf.yaml"
  log_conf_file = "log_conf.yaml"

# Gloabl variables ======================
with open(app_conf_file, 'r') as f:
  app_config = yaml.safe_load(f.read())


with open(log_conf_file, 'r') as f:
  log_config = yaml.safe_load(f.read())
  logging.config.dictConfig(log_config)
  
logger = logging.getLogger('basicLogger')
logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)


def get_health_stats():
    health = {'audit': 'Down', 'processing': 'Down', 'storage': 'Down', 'receiver': 'Down', 'Last_update': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}

    logger.info("Retrieving health stats for receiver, storage, processing and audit services")
    try:
        health_check_storage = requests.get(app_config['datastore']['storage']['url'], timeout=5)
        health['storage'] = 'Running'
    except:
        health['storage'] = 'Down'

    try:
        health_check_processing = requests.get(app_config['datastore']['processing']['url'],  timeout=5)
        health['processing'] = 'Running'
    except:
        health['processing'] = 'Down'
    try:
        health_check_audit = requests.get(app_config['datastore']['audit']['url'],  timeout=5)
        health['audit'] = 'Running'
    except:
        health['audit'] = 'Down'
    try: 
        health_check_receiver = requests.get(app_config['datastore']['receiver']['url'],  timeout=5)
        health['receiver'] = 'Running'
    except:
        health['receiver'] = 'Down'
    
    health['Last_update'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print(health)
   
    logger.info(f"All health status for all services receiverd \nHealth Status: {health}")

    # Serializing json
    json_object = json.dumps(health, indent=4)
    
    # Writing to sample.json
    with open("health.json", "w") as outfile:
        outfile.write(json_object)

    return health, 200
   

def init_scheduler():
  sched = BackgroundScheduler(daemon=True)
  sched.add_job(get_health_stats, 
                'interval', 
                seconds=app_config['exception']['sleep'])

  sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml",
                 strict_validation=True,
                validate_responses=True)

CORS(app.app)
app.app.config["CORS_HEADERS"] = "Content-Type"

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8120)
