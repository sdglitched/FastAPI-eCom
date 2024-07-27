from sqlalchemy import Column, ForeignKey, Integer, Float, Text

from sqlalchemy.orm import relationship

from fastapi_ecom.database.db_setup import Base
from fastapi_ecom.database.models.util import UUIDCreatableMixin
from fastapi_ecom.database.models.order import Order
from fastapi_ecom.database.models.product import Product

class OrderDetail(Base, UUIDCreatableMixin):
    __tablename__ = "order_details"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column("product_id", Text, ForeignKey('products.uuid'), nullable=False)
    quantity = Column("quantity", Integer, nullable=False)
    price = Column("product_price", Float, nullable=False)
    order_id = Column("order_id", Text, ForeignKey('orders.uuid', ondelete="CASCADE"), nullable=False)

    order = relationship(Order, backref="order_details", passive_deletes=True)
    product = relationship(Product, backref="order_details")
