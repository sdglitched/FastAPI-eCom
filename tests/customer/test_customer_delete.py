import pytest
from httpx import AsyncClient

from tests.customer import _test_data_customer


@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="CUSTOMER DELETE Endpoint - Deletes currently authenticated customer")
    ]
)
async def test_delete_customer(client: AsyncClient, _: None) -> None:
    """
    Test the `delete` endpoint for deleting the currently authenticated customer of the Customer
    API.

    :param client: The test client to send HTTP requests.

    :return:
    """
    """
    Get the data for testing
    """
    data = _test_data_customer()

    """
    Perform the action of visiting the endpoint
    """
    response = await client.delete("/api/v1/customer/delete/me")

    """
    Test the response
    """
    assert response.status_code == 202
    assert response.json() == {
        "action": "delete",
        "customer": {
            "email": data["delete_customer"].email,
            "name": data["delete_customer"].name,
            "addr_line_1": data["delete_customer"].addr_line_1,
            "addr_line_2": data["delete_customer"].addr_line_2,
            "city": data["delete_customer"].city,
            "state": data["delete_customer"].state
        }
    }
