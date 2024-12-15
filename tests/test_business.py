from typing import Dict

import pytest


@pytest.mark.parametrize(
    "payload, type",
    [
        pytest.param(
            {
                "email": "test_busi@example.com",
                "name": "test_busi",
                "addr_line_1": "abc",
                "addr_line_2": "xyz",
                "city": "aaa",
                "state": "bbb",
                "password": "test_busi"
            },
            "create",
            id="BUSINESS Endpoint - 201 Created",
        ),
        pytest.param(
            {
                "email": "duplicate_business@example.com",
                "name": "duplicate_business",
                "addr_line_1": "abc",
                "addr_line_2": "xyz",
                "city": "aaa",
                "state": "bbb",
                "password": "duplicate_business"
            },
            "duplicate",
            id="BUSINESS Endpoint - 409 Conflict",
        )
    ]
)
async def test_create_business(client, payload: Dict[str, str], type: str) -> None:
    """
    Test the `create` endpoint for the Business API.

    :param client: The test client to send HTTP requests.
    :param payload: A dictionary containing the data for business creation.
    :param type: A string indicating the type of test data.

    :return:

    :raises AssertionError: If the response does not match the expected status or data.
    """
    response = await client.post("/api/v1/business/create", json = payload)
    if type == "create":
        assert "business" in response.json()
        assert response.status_code == 201
    else:
        assert response.status_code == 409
        assert response.json()["detail"] == "Uniqueness constraint failed - Please try again"
