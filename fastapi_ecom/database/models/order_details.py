from sqlalchemy import Column, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from fastapi_ecom.database import baseobjc
from fastapi_ecom.database.models.util import (
    DateCreatableMixin,
    DateUpdateableMixin,
    UUIDCreatableMixin,
)


class OrderDetail(baseobjc, UUIDCreatableMixin, DateCreatableMixin, DateUpdateableMixin):
    """
    Database model representing the details of an individual item in an order.

    :cvar __tablename__: Name of the database table.
    :cvar id: Auto incremented ID for each records.
    :cvar product_id: Foreign key referencing the `Product` model.
    :cvar quantity: Quantity of the product in the order.
    :cvar price: Price of the product in the order.
    :cvar order_id: Foreign key referencing the `Order` model. The record will be deleted if the
                    associated order is deleted (CASCADE).
    :cvar orders: Relationship to the `Order` model, representing the parent order of the order
                  detail.
    :cvar products: Relationship to the `Product` model, representing the associated product in
                    the order detail.
    """
    __tablename__ = "order_details"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column("product_id", Text, ForeignKey('products.uuid'), nullable=False)
    quantity = Column("quantity", Integer, nullable=False)
    price = Column("product_price", Float, nullable=False)
    order_id = Column("order_id", Text, ForeignKey('orders.uuid', ondelete="CASCADE"), nullable=False)

    orders = relationship("Order", back_populates="order_details", passive_deletes=True)
    products = relationship("Product", back_populates="order_details")
