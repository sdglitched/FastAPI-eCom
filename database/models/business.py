from sqlalchemy import Column, Integer, String, Text, Date, Boolean
from sqlalchemy.orm import relationship

from db_setup import Base


class Business(Base):
    __tablename__ = "businesses"

    id = Column("user_id", Integer, primary_key=True, index=True)
    email = Column("email_address", String(100), unique=True, index=True, nullable=False)
    password = Column("password", String(50), nullable=False)
    name = Column("business_name", String(100), nullable=False)
    addr_line_1 = Column("address_line_1", Text, nullable=False)
    addr_line_2 = Column("address_line_2", Text, nullable=True)
    city = Column("city", Text, nullable=False)
    state = Column("state", Text, nullable=False)
    is_verified = Column("is_verified", Boolean, default=False)
    creation_date = Column("creation_date", Date, nullable=False)
    
    owner = relationship("Product", back_populates="business")

