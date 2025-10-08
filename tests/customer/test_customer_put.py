import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "payload, type",
    [
        pytest.param(
            {
                "email": "update_customer@example.com",
                "name": "update_customer",
                "addr_line_1": "abc",
                "addr_line_2": "xyz",
                "city": "aaa",
                "state": "bbb",
                "password": "update_customer",
            },
            "update",
            id="CUSTOMER PUT Endpoint - Updates currently authenticated customer",
        ),
        pytest.param(
            {
                "email": "duplicate_customer@example.com",
                "name": "duplicate_customer",
                "addr_line_1": "abc",
                "addr_line_2": "xyz",
                "city": "aaa",
                "state": "bbb",
                "password": "duplicate_customer",
            },
            "duplicate",
            id="CUSTOMER PUT Endpoint - 409 Conflict",
        ),
    ],
)
async def test_update_customer(
    client: AsyncClient, db_test_create: None, db_test_data: None, apply_security_override: None, payload: dict[str, str], type: str
) -> None:
    """
    Test the `put` endpoint for updating the currently authenticated customer of the Customer API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param apply_security_override: Fixture to set up test client with dependency override for `security`.
    :param payload: A dictionary containing the data for updating customer.
    :param type: A string indicating the type of test data.

    :return:
    """
    """
    Perform the action of visiting the endpoint
    """
    response = await client.put("/api/v1/customer/update/me", json=payload)

    """
    Test the response
    """
    if type == "update":
        assert response.status_code == 202
        assert response.json() == {
            "action": "put",
            "customer": {
                "email": payload["email"],
                "name": payload["name"],
                "addr_line_1": payload["addr_line_1"],
                "addr_line_2": payload["addr_line_2"],
                "city": payload["city"],
                "state": payload["state"],
            },
        }
    else:
        assert response.status_code == 409
        assert response.json()["detail"] == "Uniqueness constraint failed - Please try again"
