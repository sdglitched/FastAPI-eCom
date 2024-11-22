from pydantic import BaseModel


class OrderDetailsBase(BaseModel):
    """
    Base model for order detail-related schemas, providing shared configurations.
    """
    class Config:
        """
        This class enables attribute mapping from database model instances to Pydantic models
        automatically using the `from_attributes` setting.

        :cvar from_attributes: Flag that enables Pydantic to handle attribute assignment from
                               input data directly (i.e., allow assigning to the model attributes
                               directly without validation).
        """
        from_attributes = True


class OrderDetailsCreate(OrderDetailsBase):
    """
    Schema for creating new order details.

    :ivar product_id: UUID of the product associated with the order detail.
    :ivar quantity: Number of units of the product in the order.
    """
    product_id: str
    quantity: int


class OrderDetailsView(OrderDetailsCreate):
    """
    Schema for viewing order details, including additional pricing information.
    This schema inherits from `OrderDetailsCreate` to include common order details create
    attributes.

    :ivar price (float): Price of the product at the time of the order.
    """
    price: float


class OrderDetailsViewInternal(OrderDetailsView):
    """
    Internal schema for viewing order details, including unique identifiers.
    This schema inherits from `OrderDetailsView` to include common order details view attributes.

    :ivar uuid: Unique identifier for the order detail.
    """
    uuid: str


# class OrderDetailsUpdate(BaseModel):
#     product_id: Optional[str]
#     quantity: Optional[int]
