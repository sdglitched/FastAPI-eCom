from datetime import datetime, timezone
from typing import Dict

import pytest
from httpx import AsyncClient

from tests.product import _test_data_product


@pytest.mark.parametrize(
    "payload, business_id, product_id, present",
    [
        pytest.param(
            {
                "name": "Updated Test Product",
                "description": "Updated Fifth Test Product",
                "category": "updated test",
                "mfg_date": datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),#"1900-01-01 00:00:00+00:00",
                "exp_date": datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
                "price": 1950.05
            },
            "5c1c48fb",
            "10677ef1",
            True,
            id="PRODUCT PUT Endpoint - Updates the specific product of currently authenticated business",
        ),
        pytest.param(
            {
                "name": "",
                "description": "Updated Fifth Test Product",
                "category": "",
                "mfg_date": "1900-01-01 00:00:00+00:00",
                "exp_date": "1900-01-01 00:00:00+00:00",
                "price": 0.05
            },
            "5c1c48fb",
            "4e6c9aea",
            False,
            id="PRODUCT PUT Endpoint - Fails to find the specific product of currently authenticated business",
        )
    ]
)
async def test_update_product(
        client: AsyncClient,
        db_test_create: None,
        db_test_data: None,
        apply_security_override: None,
        payload: Dict[str, str],
        business_id: str,
        product_id: str,
        present: bool
) -> None:
    """
    Test the `create` endpoint of the Product API.

    :param client: The test client to send HTTP requests.
    :param db_test_create: Fixture which creates a test database.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param apply_security_override: Fixture to set up test client with dependency override for `security`.
    :param payload: A dictionary containing the data for product creation.
    :param business_id: UUID of the business whose product to be deleted.
    :param product_id: UUID of the product associated with the business which should be deleted.
    :param present: Whether the product associated with the business exists.

    :return:
    """
    """
    Get the data for assertion
    """
    data = _test_data_product()
    product = {}
    for prod in data.values():
        if prod.business_id == business_id and prod.uuid == product_id:  # uuid of authenticated business; uuid of one of their products
            product = {
                "name": prod.name,
                "description": prod.description,
                "category": prod.category,
                "mfg_date": prod.mfg_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
                "exp_date": prod.exp_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat(),
                "price": prod.price,
                "uuid": prod.uuid,
                "business_id": prod.business_id
            }

    """
    Perform the action of visiting the endpoint
    """
    response = await client.put(f"/api/v1/product/update/uuid/{product_id}", json = payload)

    """
    Test the response
    """
    if present:
        assert response.status_code == 202
        assert response.json() == {
            "action": "put",
            "product": {
                "name": payload["name"],
                "description": payload["description"],
                "category": payload["category"],
                "mfg_date": payload["mfg_date"],
                "exp_date": payload["exp_date"],
                "price": payload["price"],
                "uuid": product["uuid"],
                "business_id": product["business_id"],
            }
        }
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not present in database"
