from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from fastapi_ecom.database import baseobjc
from fastapi_ecom.database.models.util import (
    DateCreatableMixin,
    DateUpdateableMixin,
    UUIDCreatableMixin,
)


class Business(baseobjc, UUIDCreatableMixin, DateCreatableMixin, DateUpdateableMixin):
    """
    Database model representing a business entity.

    :cvar __tablename__: Name of the database table.
    :cvar id: Auto incremented ID for each records.
    :cvar email: Email address of the business, must be unique.
    :cvar password: Password for the business account.
    :cvar name: Name of the business.
    :cvar addr_line_1: Primary address line of the business.
    :cvar addr_line_2: Secondary address line of the business (optional).
    :cvar city: City where the business is located.
    :cvar state: State where the business is located.
    :cvar is_verified: Flag indicating if the business account is verified.
    :cvar oauth_provider: OAuth provider name.
    :cvar oauth_id: OAuth provider's user ID
    :cvar oauth_email: Email address from OAuth.
    :cvar created_via_oauth: Flag indicating if the business account is created using OAuth.
    :cvar products: Relationship to the `Product` model, representing the products offered by the
                    business.
    """
    __tablename__ = "businesses"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    email = Column("email_address", String(100), unique=True, index=True, nullable=False)
    password = Column("password", Text, nullable=True)
    name = Column("business_name", String(100), nullable=False)
    addr_line_1 = Column("address_line_1", Text, nullable=True)
    addr_line_2 = Column("address_line_2", Text, nullable=True)
    city = Column("city", Text, nullable=True)
    state = Column("state", Text, nullable=True)
    is_verified = Column("is_verified", Boolean, default=False)
    oauth_provider = Column("oauth_provider", String(50), nullable=True)
    oauth_id = Column("oauth_id", String(100), nullable=True)
    oauth_email = Column("oauth_email", String(100), nullable=True)
    created_via_oauth = Column("created_via_oauth", Boolean, default=False)

    products = relationship("Product", back_populates="businesses")
