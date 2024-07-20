from sqlalchemy import Column, ForeignKey, Integer, Float, Text, Date
from sqlalchemy.orm import relationship

from uuid import uuid4

from fastapi_ecom.database.db_setup import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column("order_id", Text, unique=True, nullable=False, default=uuid4().hex[0:8])
    user_id = Column("user_id", Text, ForeignKey('customers.uuid', ondelete="CASCADE"), nullable=False)
    order_date = Column("order_date", Date, nullable=False)
    total_price = Column("total_price", Float, nullable=False)

    customer = relationship("Customer", back_populates="orders", uselist=False)
    order_detail = relationship("Order_Detail", back_populates="orders")


class Order_Detail(Base):
    __tablename__ = "order_details"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column("order_id", Text, ForeignKey('orders.order_id', ondelete="CASCADE"), nullable=False)
    product_id = Column("product_id", Text, ForeignKey('products.uuid'), nullable=False)
    quantity = Column("quantity", Integer, nullable=False)
    price = Column("product_price", Float, nullable=False)

    orders = relationship("Order", back_populates="order_details", uselist=False)
    product = relationship("Product")

