from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_ecom.database.db_setup import get_db
from fastapi_ecom.database.pydantic_schemas.customer import CustomerInternal
from fastapi_ecom.database.pydantic_schemas.order import OrderCreate, OrderManyResult, OrderManyResultInternal, OrderResult, OrderResultInternal
from fastapi_ecom.utils.auth import verify_cust_cred
from fastapi_ecom.utils.crud.order import create_order, delete_order, get_all_orders, get_all_orders_internal, get_order_by_uuid


router = APIRouter(prefix="/order")

@router.post("/add", response_model=OrderResultInternal, status_code=201, tags=["order"])
async def place_order(order: OrderCreate, db: AsyncSession = Depends(get_db), customer_auth: CustomerInternal = Depends(verify_cust_cred)):
    new_order = await create_order(db=db, order=order, customer_id = customer_auth.uuid)
    return {
        "action": "post",
        "order": new_order
    }

@router.get("/search", response_model=OrderManyResult, tags=["order"])
async def read_all_orders(db: AsyncSession = Depends(get_db), customer_auth: CustomerInternal = Depends(verify_cust_cred)):
    orders = await get_all_orders(db, customer_id=customer_auth.uuid)
    return {
        "action": "get",
        "orders": orders
    }

@router.get("/search/internal", response_model=OrderManyResultInternal, tags=["order"])
async def read_all_orders_internal(db: AsyncSession = Depends(get_db)):
    orders = await get_all_orders_internal(db)
    return {
        "action": "get",
        "orders": orders
    }

@router.get("/search/uuid/{order_id}", response_model=OrderResult, tags=["order"])
async def read_order_by_uuid(order_id: str, db: AsyncSession = Depends(get_db), customer_auth: CustomerInternal = Depends(verify_cust_cred)):
    order = await get_order_by_uuid(db, customer_id=customer_auth.uuid, uuid=order_id)
    return {
        "action": "get",
        "order": order
    }

# @router.put("/update/uuid/{order_id}", response_model=OrderResult, tags=["order"])
# async def updt_order(order_id: str, order: OrderUpdate, db: AsyncSession = Depends(get_db), customer_auth: CustomerInternal = Depends(verify_cust_cred)):
#       """
#       TODO: Update endpoint will be made available one the carting system is implemented
#       """
#     order_to_update = await modify_order(db=db, uuid=order_id, customer_id=customer_auth.uuid, order=order)
#     return {
#         "action": "put",
#         "order": order_to_update
#     }

@router.delete("/delete/uuid/{order_id}", response_model=OrderResult, tags=["order"])
async def dlt_order(order_id: str, db: AsyncSession = Depends(get_db), customer_auth: CustomerInternal = Depends(verify_cust_cred)):
    order_to_delete = await delete_order(db=db, uuid=order_id, customer_id=customer_auth.uuid)
    return {
        "action": "delete",
        "order": order_to_delete
    }
