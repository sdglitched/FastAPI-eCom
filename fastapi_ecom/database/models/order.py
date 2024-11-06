from sqlalchemy import Column, ForeignKey, Integer, Float, Text, Date
from sqlalchemy.orm import relationship

from fastapi_ecom.database.db_setup import Base
from fastapi_ecom.database.models.util import DateUpdateableMixin, UUIDCreatableMixin, DateCreatableMixin


class Order(Base, UUIDCreatableMixin, DateCreatableMixin, DateUpdateableMixin):
    __tablename__ = "orders"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column("user_id", Text, ForeignKey('customers.uuid', ondelete="CASCADE"), nullable=False)
    order_date = Column("order_date", Date, nullable=False)
    total_price = Column("total_price", Float, nullable=False)

    order_details = relationship("OrderDetail", back_populates="orders")
    customers = relationship("Customer", back_populates="orders", passive_deletes=True)
