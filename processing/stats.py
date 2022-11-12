from sqlalchemy import Column, Integer, String, DateTime
from base import Base


class Stats(Base):

    __tablename__ = "stats"
    id = Column(Integer, primary_key=True)
    num_court_bookings = Column(Integer, nullable=False)
    max_court_bookings = Column(Integer, nullable=False)
    num_lesson_bookings = Column(Integer, nullable=False)
    max_lesson_bookings = Column(Integer, nullable=False)
    current_timestamp = Column(DateTime, nullable=False)
   

    def __init__(self, num_court_bookings, max_court_bookings,
        num_lesson_bookings, max_lesson_bookings,
        current_timestamp):
        """ Initializes a processing statistics objet """
        self.num_court_bookings = num_court_bookings
        self.max_court_bookings = max_court_bookings
        self.num_lesson_bookings = num_lesson_bookings
        self.max_lesson_bookings = max_lesson_bookings
        self.current_timestamp = current_timestamp
  
    def to_dict(self):
        """ Dictionary Representation of a statistics """
        dict = {}
        dict['num_court_bookings'] = self.num_court_bookings
        dict['max_court_bookings'] = self.max_court_bookings
        dict['num_lesson_bookings'] = self.num_lesson_bookings
        dict['max_lesson_bookings'] = self.max_lesson_bookings
        dict['current_timestamp'] = self.last_updated.strftime("%Y-%m-%dT%H:%M:%S")
   
        
        return dict

