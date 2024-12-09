from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from fastapi_ecom.database import baseobjc
from fastapi_ecom.database.models.util import (
    DateCreatableMixin,
    DateUpdateableMixin,
    UUIDCreatableMixin,
)


class Product(baseobjc, UUIDCreatableMixin, DateCreatableMixin, DateUpdateableMixin):
    """
    Database model representing a product offered by a business.

    :cvar __tablename__: Name of the database table.
    :cvar id: Auto incremented ID for each records.
    :cvar name: Name of the product.
    :cvar description: Description of the product (optional).
    :cvar category: Category to which the product belongs.
    :cvar mfg_date: Manufacturing date of the product.
    :cvar exp_date: Expiry date of the product.
    :cvar price: Price of the product.
    :cvar business_id: Foreign key referencing the `Business` model. If the associated business is
                       deleted, the product record will also be deleted (CASCADE).
    :cvar businesses: Relationship to the `Business` model, representing the business that sells
                      the product. The record will reflect business deletion (passive deletes).
    :cvar order_details: Relationship to the `OrderDetail` model, representing the details of
                         orders containing this product.
    """
    __tablename__ = "products"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    name = Column("product_name", String(100), nullable=False)
    description = Column("description", Text, nullable=True)
    category = Column("category", String(50), nullable=False)
    mfg_date = Column("manufacturing_date", Date, nullable=False)
    exp_date = Column("expiry_date", Date, nullable=False)
    price = Column("product_price", Float, nullable=False)
    business_id = Column("business_id", Text, ForeignKey('businesses.uuid', ondelete="CASCADE"), nullable=False)

    businesses = relationship("Business", back_populates="products", passive_deletes=True)
    order_details = relationship("OrderDetail", back_populates="products")
