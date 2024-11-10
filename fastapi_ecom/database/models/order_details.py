from sqlalchemy import Column, ForeignKey, Integer, Float, Text

from sqlalchemy.orm import relationship

from fastapi_ecom.database.db_setup import Base
from fastapi_ecom.database.models.util import DateCreatableMixin, DateUpdateableMixin, UUIDCreatableMixin


class OrderDetail(Base, UUIDCreatableMixin, DateCreatableMixin, DateUpdateableMixin):
    __tablename__ = "order_details"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column("product_id", Text, ForeignKey('products.uuid'), nullable=False)
    quantity = Column("quantity", Integer, nullable=False)
    price = Column("product_price", Float, nullable=False)
    order_id = Column("order_id", Text, ForeignKey('orders.uuid', ondelete="CASCADE"), nullable=False)

    orders = relationship("Order", back_populates="order_details", passive_deletes=True)
    products = relationship("Product", back_populates="order_details")
