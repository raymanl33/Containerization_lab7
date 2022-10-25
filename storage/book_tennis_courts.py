from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class BookTennisCourt(Base):
    """ Book Tennis Court  """

    __tablename__ = "book_tennis_court"

    id = Column(Integer, primary_key=True)
    member_id = Column(String(250), nullable=False)
    court_num = Column(Integer, nullable=False)
    member_name = Column(String(250), nullable=False)
    book_date = Column(String(100), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(250), nullable=False)
    

    def __init__(self, member_id, member_name, court_num, book_date, timestamp, trace_id):
        """ Initializes a book tennis court reading """
        self.member_id = member_id
        self.member_name = member_name
        self.court_num = court_num
        self.book_date = book_date
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a book tennis courts reading """
        dict = {}
        dict['id'] = self.id
        dict['member_id'] = self.member_id
        dict['member_name'] = self.member_name
        dict['court_num'] = self.court_num
        dict['book_date'] = self.book_date
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict