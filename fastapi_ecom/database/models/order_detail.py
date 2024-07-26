from sqlalchemy import Column, ForeignKey, Integer, Float, Text

from fastapi_ecom.database.db_setup import Base


class Order_Detail(Base):
    __tablename__ = "order_details"

    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column("order_id", Text, ForeignKey('orders.order_id', ondelete="CASCADE"), nullable=False)
    product_id = Column("product_id", Text, ForeignKey('products.uuid'), nullable=False)
    quantity = Column("quantity", Integer, nullable=False)
    price = Column("product_price", Float, nullable=False)
