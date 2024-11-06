from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from fastapi_ecom.database.db_setup import Base
from fastapi_ecom.database.models.util import DateUpdateableMixin, UUIDCreatableMixin, DateCreatableMixin


class Customer(Base, UUIDCreatableMixin, DateCreatableMixin, DateUpdateableMixin):
    __tablename__ = "customers"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    email = Column("email_address", String(100), unique=True, index=True, nullable=False)
    password = Column("password", Text, nullable=False)
    name = Column("full_name", String(100), nullable=False)
    addr_line_1 = Column("address_line_1", Text, nullable=False)
    addr_line_2 = Column("address_line_2", Text, nullable=True)
    city = Column("city", Text, nullable=False)
    state = Column("state", Text, nullable=False)
    is_verified = Column("is_verified", Boolean, default=False)

    orders = relationship("Order", back_populates="customers")
