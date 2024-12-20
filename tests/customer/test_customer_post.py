from typing import Dict

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "payload, type",
    [
        pytest.param(
            {
                "email": "test_cust@example.com",
                "name": "test_cust",
                "addr_line_1": "abc",
                "addr_line_2": "xyz",
                "city": "aaa",
                "state": "bbb",
                "password": "test_cust"
            },
            "create",
            id="CUSTOMER Post Endpoint - 201 Created",
        ),
        pytest.param(
            {
                "email": "duplicate_customer@example.com",
                "name": "duplicate_customer",
                "addr_line_1": "abc",
                "addr_line_2": "xyz",
                "city": "aaa",
                "state": "bbb",
                "password": "duplicate_customer"
            },
            "duplicate",
            id="CUSTOMER Post Endpoint - 409 Conflict",
        )
    ]
)
async def test_create_customer(client: AsyncClient, payload: Dict[str, str], type: str) -> None:
    """
    Test the `create` endpoint of the Customer API.

    :param client: The test client to send HTTP requests.
    :param payload: A dictionary containing the data for customer creation.
    :param type: A string indicating the type of test data.

    :return:

    :raises AssertionError: If the response does not match the expected status or data.
    """
    """
    Perform the action of visiting the endpoint
    """
    response = await client.post("/api/v1/customer/create", json = payload)

    """
    Test the response
    """
    if type == "create":
        assert response.status_code == 201
        assert response.json() == {
            "action": "post",
            "customer": {
                "email": payload["email"],
                "name": payload["name"],
                "addr_line_1": payload["addr_line_1"],
                "addr_line_2": payload["addr_line_2"],
                "city": payload["city"],
                "state": payload["state"]
            }
        }
    else:
        assert response.status_code == 409
        assert response.json()["detail"] == "Uniqueness constraint failed - Please try again"
