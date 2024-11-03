from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status

from sqlalchemy import and_, delete
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi_ecom.database.models.order import Order
from fastapi_ecom.database.models.order_details import OrderDetail
from fastapi_ecom.database.models.product import Product
from fastapi_ecom.database.pydantic_schemas.order import OrderCreate, OrderView, OrderViewInternal
from fastapi_ecom.database.pydantic_schemas.order_details import OrderDetailsView, OrderDetailsViewInternal


async def create_order(db: AsyncSession, order: OrderCreate, customer_id: str):
    new_order = Order(
        user_id=customer_id,
        order_date=order.order_date,
        total_price=0.0,  # Initial total, calculated below
        uuid=uuid4().hex[0:8] # Need to assign a UUID manually as the UUIDCreatableMixin stores single UUID for a transaction due to which constraint will fail
    )
    db.add(new_order)
    try:
        await db.flush()  # Generate order ID for relations
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed while commiting"
        )

    # Create OrderDetail entries and calculate the total price
    total_price = 0
    order_items = []
    for item in order.order_items:
        query = select(Product).where(Product.uuid == item.product_id)
        result = await db.execute(query)
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID: {item.product_id} does not exist."
            )
        total_price += product.price * item.quantity
        order_detail = OrderDetail(
            order_id=new_order.uuid,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price,
            uuid=uuid4().hex[0:8] # Need to assign a UUID manually as the UUIDCreatableMixin stores single UUID for a transaction due to which constraint will fail
        )
        db.add(order_detail)
        order_items.append(order_detail)

    # Update total price of the order
    new_order.total_price = total_price
    try:
        await db.flush()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed while commiting"
        )
    new_order.order_items = order_items
    return OrderViewInternal.model_validate(new_order).model_dump()

async def get_all_orders(db: AsyncSession, customer_id: str):
    """
    model_validate could not be used

    As per ChatGPT: In practice, especially with ORM models from SQLAlchemy, Pydantic sometimes
    struggles with deep nested relationshsips (like order_items in Order). This often occurs because
    SQLAlchemy relationships, loaded with .options(selectinload()), aren't automatically parsed as
    lists of model objects. When using SQLAlchemy relationships, Pydantic might misinterpret the
    fields or miss data if any nested models aren't explicitly prepared.
    """
    query = select(Order).options(selectinload(Order.order_details)).where(Order.user_id == customer_id)
    result = await db.execute(query)
    orders = result.scalars().unique().all()
    order_views = []
    for order in orders:
        order_items = [
            OrderDetailsView(
                product_id=detail.product_id,
                quantity=detail.quantity,
                price=detail.price
            )
            for detail in order.order_details
        ]
        order_view_data = OrderView(
            uuid=order.uuid,
            order_date=order.order_date,
            total_price=order.total_price,
            order_items=order_items
        )
        order_views.append(order_view_data.model_dump())

    return order_views

async def get_all_orders_internal(db: AsyncSession):
    """
    model_validate could not be used

    As per ChatGPT: In practice, especially with ORM models from SQLAlchemy, Pydantic sometimes
    struggles with deep nested relationshsips (like order_items in Order). This often occurs because
    SQLAlchemy relationships, loaded with .options(selectinload()), aren't automatically parsed as
    lists of model objects. When using SQLAlchemy relationships, Pydantic might misinterpret the
    fields or miss data if any nested models aren't explicitly prepared.
    """
    query = select(Order).options(selectinload(Order.order_details))
    result = await db.execute(query)
    orders = result.scalars().unique().all()
    order_views = []
    for order in orders:
        order_items = [
            OrderDetailsViewInternal(
                product_id=detail.product_id,
                quantity=detail.quantity,
                price=detail.price,
                uuid=detail.uuid
            )
            for detail in order.order_details
        ]
        order_view_data = OrderViewInternal(
            uuid=order.uuid,
            user_id=order.user_id,
            order_date=order.order_date,
            total_price=order.total_price,
            order_items=order_items
        )
        order_views.append(order_view_data.model_dump())

    return order_views

async def get_order_by_uuid(db: AsyncSession, customer_id: str, uuid: str):
    query = select(Order).options(selectinload(Order.order_details)).where(and_(Order.user_id == customer_id, Order.uuid == uuid))
    result = await db.execute(query)
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not present in database"
        )
    order_items = [
        OrderDetailsView(
            product_id=detail.product_id,
            quantity=detail.quantity,
            price=detail.price
        )
        for detail in order.order_details
    ]
    order_view = OrderView(
        uuid=order.uuid,
        order_date=order.order_date,
        total_price=order.total_price,
        order_items=order_items
    )
    return OrderView.model_validate(order_view).model_dump()

# async def modify_order(db: AsyncSession, order: OrderUpdate, uuid: str, customer_id: str):
#     """
#     TODO: Modify function will be made available one the carting system is implemented
#     """
#     pass

async def delete_order(db: AsyncSession, uuid: str, customer_id: str):
    order_to_delete = await get_order_by_uuid(db=db, uuid=uuid, customer_id=customer_id)
    query = delete(Order).filter_by(uuid=uuid)
    await db.execute(query)
    try:
        await db.flush()
    except IntegrityError as expt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed while deleting"
        )
    return OrderView.model_validate(order_to_delete)