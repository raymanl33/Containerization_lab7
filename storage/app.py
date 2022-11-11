import connexion 
from connexion import NoContent 
import json
import datetime
import os
from base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from book_tennis_courts import BookTennisCourt
from book_tennis_lessons import BookTennisLesson
import yaml
import pymysql
import logging
import logging.config
#from dateutil import parser
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread 
from sqlalchemy import and_

with open('app_conf.yml', 'r') as f:
  app_config = yaml.safe_load(f.read())


with open('log_conf.yaml', 'r') as f:
  log_config = yaml.safe_load(f.read())
  logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


user = app_config['datastore']['user']
password = app_config['datastore']['password']
hostname = app_config['datastore']['hostname']
port = app_config['datastore']['port']
db = app_config['datastore']['db']

create_engine_str = f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}'

DB_ENGINE = create_engine(create_engine_str)
Base.metadata.bind = DB_ENGINE
Base.metadata.create_all(DB_ENGINE)
DB_SESSION = sessionmaker(bind=DB_ENGINE)

logger.info(f"Connecting to DB. Hostname:{hostname}, Port:{port}")
def get_court_bookings(timestamp, end_timestamp):
  """ Gets new tennis court bookings after the timestamp """

  session = DB_SESSION()
  print(timestamp)
  timestamp_datetime = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

  end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

  readings = session.query(BookTennisCourt).filter(
    and_(BookTennisCourt.date_created >= timestamp_datetime,
    BookTennisCourt.date_created < end_timestamp_datetime))
  
  results_list = []

  for reading in readings:
    results_list.append(reading.to_dict())
  # print(results_list)
  session.close()

  logger.info("Query for tennis court bookings after %s return %d results" %(timestamp_datetime, len(results_list)))

  return results_list, 200


def get_tennis_lessons(timestamp, end_timestamp):
  """ Gets new tennis court bookings after the timestamp """

  session = DB_SESSION()
  print(timestamp)
  timestamp_datetime = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
  end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

  readings = session.query(BookTennisLesson).filter(
    and_(BookTennisLesson.date_created >= timestamp_datetime,
        BookTennisLesson.date_created < end_timestamp_datetime))
  
  results_list = []

  for reading in readings:

    results_list.append(reading.to_dict())
  # print(results_list)
  session.close()
  
  logger.info("Query for tennis lesson bookings after %s return %d results" %(timestamp_datetime, len(results_list)))

  return results_list, 200



def process_messages():
  """ Process event messages """

  hostname = "%s:%d" % (app_config["events"]["hostname"],
                        app_config["events"]["port"])

  client = KafkaClient(hosts=hostname)
  topic = client.topics[str.encode(app_config["events"]["topic"])]
  # Create a consume on a cosumer group, that only reads new messages 
  # (uncommitted messages) when  the service re-starts (i.e., it doesnt 
  # read all the old messages from the history in the message queue).
  consumer = topic.get_simple_consumer(consumer_group=b'event_group', reset_offset_on_start=False, auto_offset_reset=OffsetType.LATEST)

  # This is blocking - it will wait for a new message
  for msg in consumer: 
    msg_str = msg.value.decode('utf-8')
    msg = json.loads(msg_str)
    logger.info("Message: %s" % msg)

    payload = msg["payload"]

    if msg["type"] == "book_tennis_lesson": # Change this to your event type 
      # Store the event1 (i.e., the payload) to the DB 
      session = DB_SESSION()
      
      btl = BookTennisLesson(msg['payload']['memberID'],
                        msg['payload']['lessonDate'],
                        msg['payload']['memberName'],
                        msg['payload']['coachName'],
                        msg['payload']['lessonRate'],
                        msg['payload']['lessonDate'],
                        msg['payload']['trace_id'])
                      
      session.add(btl)

      session.commit()
      session.close()

      trace_id = msg['payload']['trace_id']
      logger.info(f'Stored event book tennis event request with a trace id of {trace_id}')
      print('event1') 
    elif msg["type"] == "book_tennis_court":
      # Store the event2 (i.e., the payload) to the DB
   
      session = DB_SESSION()

      bc = BookTennisCourt(msg['payload']['memberID'],
                        msg['payload']['memberName'],
                        msg['payload']['courtNum'],
                        msg['payload']['bookDate'],
                        msg['payload']['bookDate'],
                        msg['payload']['trace_id'])

      session.add(bc)

      session.commit()
      session.close()
      trace_id = msg['payload']['trace_id']
      logger.info(f'Stored event book tennis event request with a trace id of {trace_id}')

    # Commit the new message as being read
    consumer.commit_offsets()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml",
                 strict_validation=True,
                validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
    
