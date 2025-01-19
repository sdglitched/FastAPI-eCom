from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.product import _test_data_product


@pytest.mark.parametrize(
    "business_id, product_id, present",
    [
        pytest.param("5c1c48fb", "d5cf6983", True, id="PRODUCT DELETE Endpoint - Deletes the specific product of currently authenticated business"),
        pytest.param("5c1c48fb", "d76a11f2", False, id="PRODUCT DELETE Endpoint - Fails to find the specific product of currently authenticated business"),
    ]
)
async def test_delete_product(
        client: AsyncClient,
        db_test_data: AsyncGenerator[AsyncSession, None],
        apply_security_override,
        business_id: str,
        product_id: str,
        present: bool
) -> None:
    """
    Test the `delete` endpoint for deleting the specific product associated with the authenticated
    business of the Product API.

    :param client: The test client to send HTTP requests.
    :param db_test_data: Fixture to populate the test database with initial test data.
    :param apply_security_override: Fixture to set up test client with dependency override for `security`.
    :param business_id: UUID of the business whose product to delete.
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
        if prod.business_id == business_id and prod.uuid == product_id:  #uuid of authenticated business; uuid of one of their products
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
    response = await client.delete(f"/api/v1/product/delete/uuid/{product_id}")

    """
    Test the response
    """
    if present:
        assert response.status_code == 202
        assert response.json() == {
            "action": "delete",
            "product": product
        }
    else:
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not present in database"
