from sqlalchemy import Column, ForeignKey, Integer, Float, Text, Date

from uuid import uuid4

from fastapi_ecom.database.db_setup import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column("order_id", Text, unique=True, nullable=False, default=uuid4().hex[0:8])
    user_id = Column("user_id", Text, ForeignKey('customers.uuid', ondelete="CASCADE"), nullable=False)
    order_date = Column("order_date", Date, nullable=False)
    total_price = Column("total_price", Float, nullable=False)
