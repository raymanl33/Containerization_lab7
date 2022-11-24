import connexion 
from connexion import NoContent 
import json
import datetime
import os
import requests
import yaml
import logging
import logging.config
import uuid
from pykafka import KafkaClient
import time 

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
  print("In Test Environment")
  app_conf_file = "/config/app_conf.yaml"
  log_conf_file = "/config/log_conf.yaml"
else:
  print("In Dev Environment")
  app_conf_file = "app_conf.yaml"
  log_conf_file = "log_conf.yaml"

# Gloabl variables ======================
# External Loggin Configuration
with open(app_conf_file, 'r') as f:
  app_config = yaml.safe_load(f.read())

with open(log_conf_file, 'r') as f:
  log_config = yaml.safe_load(f.read())
  logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')
logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

# Gloabl variables ======================
maximum_retries = app_config['exception']['retry_limit']
current_count = 0
sleep_time = app_config['exception']['sleep']

while current_count < maximum_retries:
  try:
      logger.info(f"Trying to connect to Kafka\n  Current retry count: {current_count}")
      client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
      topic = client.topics[str.encode(app_config['events']['topic'])]
      producer = topic.get_sync_producer()
      break
      
    
  except Exception as e:
    logger.error(f"Connection to Kafka Failed {e}")
    time.sleep(sleep_time)
    current_count += 1

def health():
  """ get the status of the  """
  return 200

def book_tennis_court(body):

  """ Recevies a tennis booking request """
  trace_id = uuid.uuid4()

  logger.info(f'Received book tennis lesson court event request with a trace id of {str(trace_id)}')
  url = app_config['eventstore1']['url']

  tennis_booking_data = {
  "bookDate": body['bookDate'],
  "courtNum": body['courtNum'],
  "memberID": body['memberID'],
  "memberName": body['memberName'],
  "trace_id" : str(trace_id)
  }

  

  msg = {"type": "book_tennis_court", 
  "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), 
  "payload": tennis_booking_data }
  msg_str = json.dumps(msg)
  producer.produce(msg_str.encode('utf-8'))

  # hard code status code to 201
  response = 201

  if response == 201:
    logger.info(f'Returned event book tennis lesson response {str(trace_id)} with status {response}')


  return NoContent, 201



def book_tennis_lesson(body):
  """ Receives a tennis booking lesson request """
  trace_id = uuid.uuid4()
  logger.info(f'Received event book tennis lesson request with a trace id of {str(trace_id)}')
  url = app_config['eventstore2']['url']


  

  tennisLesson_booking_data = {
  "coachName":  body['coachName'],
  "lessonDate":  body['lessonDate'],
  "lessonRate":  body['lessonRate'],
  "memberID":  body['memberID'],
  "memberName":  body['memberName'],
  "trace_id" : str(trace_id)
  }

  msg = {"type": "book_tennis_lesson", 
  "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), 
  "payload": tennisLesson_booking_data }
  msg_str = json.dumps(msg)
  producer.produce(msg_str.encode('utf-8'))
  
  # hard code status code to 201
  response = 201
  
  if response == 201:
    logger.info(f'Returned event book tennis lesson response {str(trace_id)} with status {response}')


  return NoContent, 201
            


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml", base_path="/receiver",
                 strict_validation=True,
                validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)