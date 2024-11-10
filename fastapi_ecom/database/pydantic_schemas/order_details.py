from abc import ABC
from typing import List, Optional

from pydantic import BaseModel


class OrderDetailsBase(BaseModel, ABC):
    """
    Base: OrderDetails
    """

    class Config:
        from_attributes = True


class OrderDetailsCreate(OrderDetailsBase):
    product_id: str
    quantity: int


class OrderDetailsView(OrderDetailsCreate):
    price: float


class OrderDetailsViewInternal(OrderDetailsView):
    uuid: str
    

# class OrderDetailsUpdate(BaseModel):
#     product_id: Optional[str]
#     quantity: Optional[int]
