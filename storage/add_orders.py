from sqlalchemy import Column, Integer, String, DateTime, Float
from base import Base
import datetime


class AddOrder(Base):
    """ Add Orders """

    __tablename__ = "add_orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(String(250), nullable=False)
    order_id = Column(String(250), nullable=False)
    restaurant = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    order_total = Column(Float, nullable=False)

    def __init__(self, customer_id, order_id, restaurant, order_total, timestamp):
        """ Initializes a food order """
        self.customer_id = customer_id
        self.order_id = order_id
        self.restaurant = restaurant
        self.timestamp = timestamp
        self.order_total = order_total
        # Sets the date/time record is created
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of adding a food order """
        dict = {}
        dict['id'] = self.id
        dict['customer_id'] = self.customer_id
        dict['order_id'] = self.order_id
        dict['restaurant'] = self.restaurant
        dict['order_total'] = self.order_total
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created

        return dict
