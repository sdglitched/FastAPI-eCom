from sqlalchemy import Column, ForeignKey, Integer, Float, String, Text, Date
from sqlalchemy.orm import relationship

from db_setup import Base


class Product(Base):
    __tablename__ = "products"

    id = Column("product_id", Integer, primary_key=True, index=True)
    name = Column("product_name", String(100), nullable=False)
    description = Column("description", Text, nullable=True)
    category = Column("category", String(50), nullable=False)
    mfg_date = Column("manufacturing_date", Date, nullable=False)
    exp_date = Column("expiry_date", Date, nullable=False)
    price = Column("product_price", Float, nullable=False)
    user_id = Column("user_id", Integer, ForeignKey('businesses.user_id', ondelete="CASCADE"), nullable=False)
    
    business = relationship("Business", back_populates="owner", uselist=False)