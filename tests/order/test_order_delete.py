
import pytest
from httpx import AsyncClient

from tests.order import _test_data_order_details, _test_data_orders


@pytest.mark.parametrize(
    "order_id, present",
    [
        pytest.param("375339b1", True, id="ORDER DELETE Endpoint - Delete a specified order of the authenticated customer"),
        pytest.param("xxxx1111", False, id="ORDER DELETE Endpoint - Fail to delete a specified order of the authenticated customer")
    ]
)
async def test_delete_order(
        client: AsyncClient,
        db_test_create: None,
        db_test_data: None,
        apply_security_override: None,
        order_id: str,
        present: str
) -> None:
    """
    Test the `delete` endpoint for deleting a specified order of the Order API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param apply_security_override: Fixture to set up test client with dependency override for `security`.
    :param order_id: The UUID of the specific order.
    :param present: A boolean indicating presence of orders for the authenticated customer.

    :return:
    """
    """
    Get the data for assertion
    """
    ords = _test_data_orders()
    order_details = _test_data_order_details()
    for ord in ords.values():
        if ord.uuid == order_id:
            order_items = [
                {
                    "product_id": detail.product_id,
                    "quantity": detail.quantity,
                    "price": detail.price
                } for detail in order_details.values()
                if detail.order_id == ord.uuid
            ]
            total_price = sum(item["quantity"] * item["price"] for item in order_items)
            order = {
                "uuid": ord.uuid,
                "order_date": ord.order_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
                "total_price": total_price,
                "order_items": order_items
            }

    """
    Perform the action of visiting the endpoint
    """
    response = await client.delete(f"/api/v1/order/delete/uuid/{order_id}")

    """
    Test the response
    """
    if present:
        assert response.status_code == 202
        assert response.json() == {
            "action": "delete",
            "order": order
        }
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "Order not present in database"
