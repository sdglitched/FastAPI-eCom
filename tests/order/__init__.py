from datetime import datetime, timezone

from fastapi_ecom.database.models.order import Order
from fastapi_ecom.database.models.order_details import OrderDetail


def _test_data_orders() -> dict[str, Order]:
    """
    Provides test data for testing the order endpoint.

    :return: A dictionary containing Order objects for testing.
    """
    data = {
        "test_order1": Order(
            uuid="feb2f4fa",  #Specific UUID for testing
            user_id="2c92f0e8",  #UUID from customer test data
            order_date=datetime.now(timezone.utc),
            total_price=590.0
        ),
        "test_order2": Order(
            uuid="375339b1",  #Specific UUID for testing
            user_id="2b203687",  #UUID from customer test data
            order_date=datetime.now(timezone.utc),
            total_price=700.0
        )
    }
    return data

def _test_data_order_details() -> dict[str, OrderDetail]:
    """
    Provides test data for testing the order endpoint.

    :return: A dictionary containing OrderDetail objects for testing.
    """
    data = {
        "test_order_detail_1a": OrderDetail(
            uuid="8e9a7e8f",  #Specific UUID for testing
            product_id="3250fcbe",  #UUID from product test data
            quantity=5,
            price=100.0,
            order_id="feb2f4fa"  #UUID from order test data
        ),
        "test_order_detail_1b": OrderDetail(
            uuid="4e88e56f",  #Specific UUID for testing
            product_id="2e7a5e2d",  #UUID from product test data
            quantity=9,
            price=10.0,
            order_id="feb2f4fa"  #UUID from order test data
        ),
        "test_order_detail_2a": OrderDetail(
            uuid="9ecec3de",  #Specific UUID for testing
            product_id="2e7a5e2d",  #UUID from product test data
            quantity=10,
            price=70.0,
            order_id="375339b1"  #UUID from order test data
        )
    }
    return data
