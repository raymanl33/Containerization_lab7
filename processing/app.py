import connexion 
from connexion import NoContent 
import requests
import json
import datetime
import os
import yaml
import logging
import logging.config
import uuid
import os
from base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler
from os.path import exists
import ast
from stats import Stats
from flask_cors import CORS, cross_origin
import sqlite3

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

sqlite_file = app_config['datastore']['filename']

# Check if sqlite file exists
if os.path.isfile(sqlite_file) == False:
  create_engine(sqlite_file)

def create_database(sqlite_file):
  

  conn = sqlite3.connect('data.sqlite')


  c = conn.cursor()
  c.execute('''
          CREATE TABLE stats
          (id INTEGER PRIMARY KEY ASC,
          num_court_bookings INTEGER NOT NULL,
          max_court_bookings INTEGER NOT NULL,
          num_lesson_bookings INTEGER NOT NULL,
          max_lesson_bookings INTEGER NOT NULL,
          last_updated VARCHAR(100) NOT NULL),
          current VARCHAR (100) NOT NULL
          ''' )

  conn.commit()
  conn.close()



DB_ENGINE = create_engine(f"sqlite:///{sqlite_file}")
Base.metadata.bind = DB_ENGINE
Base.metadata.create_all(DB_ENGINE)
DB_SESSION = sessionmaker(bind=DB_ENGINE)

# Gloabl variables ======================


def get_stats():
  """ Gets new tennis court bookings after the timestamp """
  logger.info("Request started")
  session = DB_SESSION()

  results = session.query(Stats).order_by(Stats.last_updated.desc())

  results_list = []

  for result in results:
    results_list.append(result.to_dict())

  if results_list:
    print(results_list[0])


    return results_list[0], 200

  else:
    logger.error("Statistics do not exist")
    return 404
  

  session.close()

def pupulate_stats():
  """ Periodically update stats """

  # Log an INFO message indicating periodic processing has started 
  logger.info("Start Periodic Processing")
  url = app_config['eventstore']['url']
  session = DB_SESSION()
  results = session.query(Stats).all()
  if not results:
    
    

    bc = Stats(0,100,0,100,datetime.datetime.now())

    session.add(bc)

    session.commit()
    session.close()

    return NoContent, 201

  else:

    session = DB_SESSION()
    results = session.query(Stats).order_by(Stats.last_updated.desc())



    session.close()
   
    # timestamp_datetime = datetime.datetime.strptime(results[0].last_updated, '%Y-%m-%dT%H:%M:%S')
    # print(timestamp_datetime)
    last_updated = results[0].last_updated.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z"
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z"

    print(current_timestamp)
    # Query the two GET endpoints from your Data Store Serviec (Using requests.get) 
    tennis_lessons_response = requests.get(f"{url}/TennisLessons?timestamp={last_updated}&end_timestamp={current_timestamp}")
    tennis_courts_response = requests.get(f"{url}/courtBookings?timestamp={last_updated}&end_timestamp={current_timestamp}")

    

    if tennis_lessons_response.status_code != 200:
      logger.error(f"ERROR!! got the staus code of {tennis_lessons_response.status_code}")
      
    elif tennis_courts_response.status_code != 200 : 
      logger.error(f"ERROR!! got the staus code of {tennis_courts_response.status_code}")
    else:
      logger.info(f"2 number of events received")

    # Log a DEBUG message for each event processed that includes the trace_id
    tennis_lessons_response_li = ast.literal_eval(tennis_lessons_response.text)
    tennis_courts_response_li = ast.literal_eval(tennis_courts_response.text)
    stats = {"num_court_bookings": results[0].num_court_bookings, "num_lesson_bookings": results[0].num_lesson_bookings}


    for lessons_response in tennis_lessons_response_li:
    
      if lessons_response['trace_id']:
        logger.debug(f"tennis lessons trace_id identified {lessons_response['trace_id']}")
        stats['num_lesson_bookings'] += 1
      
    for courts_response in tennis_courts_response_li:
      if courts_response['trace_id']:
        logger.debug(f"tennis courts trace_id identified: {courts_response['trace_id']}")
        stats['num_court_bookings'] += 1
    
    

    session = DB_SESSION()
    current_timestamp = datetime.datetime.strptime(current_timestamp,'%Y-%m-%dT%H:%M:%S.%fZ')
    bc = Stats(stats['num_court_bookings'],
              100,
              stats['num_lesson_bookings'],
              100,
              current_timestamp
             
              )

    logger.debug(f"Updated statitics values num_courts_bookings: {stats['num_court_bookings']}, max_num_court_bookings: {100}, num_lessons_bookings: {stats['num_lesson_bookings']}, max_lessons_bookings: {100}")
    session.add(bc)

    session.commit()
    
    session.close()
    logger.info("Period processing has ended")
    return NoContent, 201
  


def init_scheduler():
  sched = BackgroundScheduler(daemon=True)
  sched.add_job(pupulate_stats, 
                'interval', 
                seconds=app_config['scheduler']['period_sec'])

  sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml",
                 strict_validation=True,
                validate_responses=True)

CORS(app.app)
app.app.config["CORS_HEADERS"] = "Content-Type"

if __name__ == "__main__":
  # run our standalone gevent server
  init_scheduler()
  app.run(port=8100, use_reloader=False)
