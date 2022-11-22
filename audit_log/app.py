import connexion 
import os
from connexion import NoContent 
import json
from pykafka import KafkaClient
import yaml
import logging
import logging.config
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

def health():
  """ get the status of the  """
  return 200


def get_court_bookings_reading(index):
    """ Get Tennis court booking in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
 

    logger.info("Retrieving Tennis Court Booking at index %d" % index)
    try:
        count = 0
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
       
            if msg['type'] == "book_tennis_court" and count == index:
                print(msg)
                
                return msg, 200
            elif msg['type'] != "book_tennis_court":
                continue
            else: 
                # print(msg)
                count += 1
          
            # Find the event at the index you want and
            # return code 200
            # i.e., return event, 200
    except:
        logger.error("No more messages found")
    logger.error("Could not find Tennis Court Booking at index %d" % index)

    return { "message": "Not Found"}, 404
def get_tennis_lessons_reading(index):
    
    """ Get Tennis lesson booking in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)


    logger.info("Retrieving Tennis Lesson Booking at index %d" % index)
    try:
        count = 0
     
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == "book_tennis_lesson" and count == index:
                print(msg)
                return msg, 200
            elif msg['type'] != "book_tennis_lesson":
                continue
            else: 
                count += 1
            # Find the event at the index you want and
            # return code 200
            # i.e., return event, 200
    except:
        logger.error("No more messages found")
    logger.error("Could not find Tennis Lesson Booking at index %d" % index)
    
    return { "message": "Not Found"}, 404


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml",
                 strict_validation=True,
                validate_responses=True)

CORS(app.app)
app.app.config["CORS_HEADERS"] = "Content-Type"

if __name__ == "__main__":
    app.run(port=9080)
