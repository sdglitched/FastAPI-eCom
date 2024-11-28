from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from fastapi_ecom.database.db_setup import Base
from fastapi_ecom.database.models.util import (
    DateCreatableMixin,
    DateUpdateableMixin,
    UUIDCreatableMixin,
)


class Customer(Base, UUIDCreatableMixin, DateCreatableMixin, DateUpdateableMixin):
    """
    Database model representing a customer entity.

    :cvar __tablename__: Name of the database table.
    :cvar id: Auto incremented ID for each records.
    :cvar email: Email address of the customer, must be unique.
    :cvar password: Password for the customer account.
    :cvar name: Full name of the customer.
    :cvar addr_line_1: Primary address line of the customer.
    :cvar addr_line_2: Secondary address line of the customer (optional).
    :cvar city: City where the customer resides.
    :cvar state: State where the customer resides.
    :cvar is_verified: Flag indicating if the customer account is verified.
    :cvar orders: Relationship to the `Order` model, representing orders placed by the customer.
    """
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
