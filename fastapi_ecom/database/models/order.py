from sqlalchemy import Column, Date, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from fastapi_ecom.database.db_setup import Base
from fastapi_ecom.database.models.util import (
    DateCreatableMixin,
    DateUpdateableMixin,
    UUIDCreatableMixin,
)


class Order(Base, UUIDCreatableMixin, DateCreatableMixin, DateUpdateableMixin):
    """
    Database model representing an order placed by a customer.

    :cvar __tablename__: Name of the database table.
    :cvar id: Auto incremented ID for each records.
    :cvar user_id: Foreign key referencing the `Customer` model. If the associated customer is
                   deleted, the record will also be deleted (CASCADE).
    :cvar order_date: Date when the order was placed.
    :cvar total_price: Total price of all items in the order.
    :cvar order_details: Relationship to the `OrderDetail` model, representing the details of
                         products included in the order.
    :cvar customers: Relationship to the `Customer` model, representing the customer who placed the
                     order. The record will reflect customer deletion (passive deletes).
    """
    __tablename__ = "orders"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column("user_id", Text, ForeignKey('customers.uuid', ondelete="CASCADE"), nullable=False)
    order_date = Column("order_date", Date, nullable=False)
    total_price = Column("total_price", Float, nullable=False)

    order_details = relationship("OrderDetail", back_populates="orders")
    customers = relationship("Customer", back_populates="orders", passive_deletes=True)
