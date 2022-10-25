from sqlalchemy import Column, Integer, String, DateTime
from base import Base


class Stats(Base):

    __tablename__ = "stats"
    id = Column(Integer, primary_key=True)
    num_court_bookings = Column(Integer, nullable=False)
    max_court_bookings = Column(Integer, nullable=False)
    num_lesson_bookings = Column(Integer, nullable=False)
    max_lesson_bookings = Column(Integer, nullable=False)
    last_updated = Column(DateTime, nullable=False)

    def __init__(self, num_court_bookings, max_court_bookings,
        num_lesson_bookings, max_lesson_bookings,
        last_updated):
        """ Initializes a processing statistics objet """
        self.num_court_bookings = num_court_bookings
        self.max_court_bookings = max_court_bookings
        self.num_lesson_bookings = num_lesson_bookings
        self.max_lesson_bookings = max_lesson_bookings
        self.last_updated = last_updated
    def to_dict(self):
        """ Dictionary Representation of a statistics """
        dict = {}
        dict['num_court_bookings'] = self.num_court_bookings
        dict['max_court_bookings'] = self.max_court_bookings
        dict['num_lesson_bookings'] = self.num_lesson_bookings
        dict['max_lesson_bookings'] = self.max_lesson_bookings
        dict['last_updated'] = self.last_updated.strftime("%Y-%m-%dT%H:%M:%S")
        
        return dict

