from datetime import datetime, timezone

from fastapi_ecom.database.models.product import Product


def _test_data_product() -> dict[str, Product]:
    """
    Provides test data for testing the product endpoint.

    :return: A dictionary containing Product objects for testing.
    """
    data = {
        "test_prod_1": Product(
            name="test_prod_1",
            description="First Test Product",
            category="test",
            mfg_date=datetime.now(timezone.utc),
            exp_date=datetime.now(timezone.utc),
            price=100.0,
            business_id="d76a11f2",
            uuid="3250fcbe"  #Specific UUID for testing of Product Endpoint
        ),
        "test_prod_2": Product(
            name = "test_prod_2",
            description = "Second Test Product",
            category = "test",
            mfg_date=datetime.now(timezone.utc),
            exp_date=datetime.now(timezone.utc),
            price = 250.0,
            business_id="d76a11f2",
            uuid="4e6c9aea"  #Specific UUID for testing of Product Endpoint
        ),
        "test_prod_3": Product(
            name = "test_prod_3",
            description = "Third Test Product",
            category = "test",
            mfg_date=datetime.now(timezone.utc),
            exp_date=datetime.now(timezone.utc),
            price = 115.0,
            business_id="d76a11f2",
            uuid="2e7a5e2d"   #Specific UUID for testing of Product Endpoint
        ),
        "test_prod_4": Product(
            name="test_prod_4",
            description="Fourth Test Product",
            category="test",
            mfg_date=datetime.now(timezone.utc),
            exp_date=datetime.now(timezone.utc),
            price=25.0,
            business_id="5c1c48fb",
            uuid="d5cf6983"  # Specific UUID for testing of Product Endpoint
        ),
        "test_prod_5": Product(
            name="test_prod_5",
            description="Fifth Test Product",
            category="test",
            mfg_date=datetime.now(timezone.utc),
            exp_date=datetime.now(timezone.utc),
            price=65.0,
            business_id="5c1c48fb",
            uuid="10677ef1"  # Specific UUID for testing of Product Endpoint
        )
    }
    return data
