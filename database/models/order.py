from sqlalchemy import Column, ForeignKey, Integer, Float, Date
from sqlalchemy.orm import relationship

from db_setup import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column("order_id", Integer, primary_key=True, index=True)
    user_id = Column("user_id", Integer, ForeignKey('customers.user_id', ondelete="CASCADE"), nullable=False)
    order_date = Column("order_date", Date, nullable=False)
    total_price = Column("total_price", Float, nullable=False)

    customer = relationship("Customer", back_populates="orders", uselist=False)
    order_detail = relationship("Order_Detail", back_populates="orders")


class Order_Detail(Base):
    __tablename__ = "order_details"

    order_id = Column("order_id", Integer, ForeignKey('orders.order_id', ondelete="CASCADE"), nullable=False)
    product_id = Column("product_id", Integer, ForeignKey('products.product_id'), nullable=False)
    quantity = Column("quantity", Integer, nullable=False)
    price = Column("product_price", Float, nullable=False)

    orders = relationship("Order", back_populates="order_details", uselist=False)
    product = relationship("Product")

