from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class BookTennisLesson(Base):
    """ Book tennis lesson  """

    __tablename__ = "book_tennis_lesson"

    id = Column(Integer, primary_key=True)
    member_id = Column(String(250), nullable=False)
    lesson_date = Column(String(250), nullable=False)
    member_name = Column(String(250), nullable=False)
    coach_name = Column(String(250), nullable=False)
    lesson_rate = Column(Float, nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, member_id, lesson_date, member_name,coach_name,lesson_rate,timestamp, trace_id):
        """ Initializes a tennis lesson booking reading """
        self.member_id = member_id
        self.lesson_date = lesson_date
        self.member_name = member_name
        self.coach_name = coach_name
        self.lesson_rate = lesson_rate
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()

        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a book tennis lesson reading """
        dict = {}
        dict['id'] = self.id
        dict['member_id'] = self.member_id
        dict['lesson_date'] = self.lesson_date
        dict['member_name'] = self.member_name
        dict['coach_name'] = self.coach_name
        dict['lesson_rate'] = self.lesson_rate
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id
        return dict
