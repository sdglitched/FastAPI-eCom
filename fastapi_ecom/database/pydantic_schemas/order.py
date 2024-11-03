from abc import ABC
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from fastapi_ecom.database.pydantic_schemas.order_details import OrderDetailsCreate, OrderDetailsView, OrderDetailsViewInternal
from fastapi_ecom.database.pydantic_schemas.util import APIResult


class OrderBase(BaseModel, ABC):
    """
    Base: Order
    """

    class Config:
        from_attributes = True


class OrderCreate(OrderBase):
    order_date: datetime
    order_items: List[OrderDetailsCreate]


class OrderView(OrderCreate):
    uuid: str
    total_price: float
    order_items: List[OrderDetailsView]


class OrderViewInternal(OrderView):
    user_id: str
    order_items: List[OrderDetailsViewInternal]


# class OrderUpdate(BaseModel):
#     order_items: Optional[List[OrderDetailsUpdate]]


class OrderResult(APIResult):
    order: OrderView


class OrderResultInternal(APIResult):
    order: OrderViewInternal


class OrderManyResult(APIResult):
    orders: List[OrderView] = []


class OrderManyResultInternal(APIResult):
    orders: List[OrderViewInternal] = []
