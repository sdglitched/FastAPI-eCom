from sqlalchemy import Column, ForeignKey, Integer, Float, String, Text, Date
from sqlalchemy.orm import relationship

from fastapi_ecom.database.db_setup import Base
from fastapi_ecom.database.models.util import DateCreatableMixin, DateUpdateableMixin, UUIDCreatableMixin


class Product(Base, UUIDCreatableMixin, DateCreatableMixin, DateUpdateableMixin):
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
