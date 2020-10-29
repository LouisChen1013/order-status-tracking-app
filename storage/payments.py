from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Payment(Base):
    """ Payment"""

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(250), nullable=False)
    payment_id = Column(String(250), nullable=False)
    restaurant = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, customer_id, payment_id, restaurant, timestamp):
        """ Initializes a payment """
        self.customer_id = customer_id
        self.payment_id = payment_id
        self.restaurant = restaurant
        self.timestamp = timestamp
        # Sets the date/time record is created
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a payment """
        dict = {}
        dict['id'] = self.id
        dict['customer_id'] = self.customer_id
        dict['payment_id'] = self.payment_id
        dict['restaurant'] = self.restaurant
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created

        return dict
