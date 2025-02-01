
import pytest
from httpx import AsyncClient

from tests.customer import _test_data_customer


@pytest.mark.parametrize(
    "_",
    [
        pytest.param(None, id="CUSTOMER DELETE Endpoint - Deletes currently authenticated customer")
    ]
)
async def test_delete_customer(
        client: AsyncClient,
        db_test_create: None,
        db_test_data: None,
        apply_security_override: None,
        _: None
) -> None:
    """
    Test the `delete` endpoint for deleting the currently authenticated customer of the Customer
    API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param apply_security_override: Fixture to set up test client with dependency override for `security`.

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
