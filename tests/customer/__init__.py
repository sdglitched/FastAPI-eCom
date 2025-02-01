from typing import Dict

from fastapi_ecom.database.models.customer import Customer


def _test_data_customer() -> Dict[str, Customer]:
    """
    Provides test data for testing the customer endpoint.

    :return: A dictionary containing Customer objects for testing.
    """
    data = {
        "test_customer": Customer(
            email="test_customer@example.com",
            password="$2b$12$cP3LsL.tlDCRczXcOPjoie74MmDAxgB0lnYUQXF98lkFVoM49gHzW",  #Hashed password
            name="test_customer",
            addr_line_1="abc",
            addr_line_2="xyz",
            city="aaa",
            state="bbb",
            uuid="2c92f0e8"  #Specific UUID for testing of Order Endpoint
        ),
        "duplicate_customer": Customer(
            email="duplicate_customer@example.com",
            password="$2b$12$Gzw8nGR9x/CxcC0jxNtqAu58NbrtcjBRO9MDH4WMerAeRDkl8vKBC",  #Hashed password
            name="duplicate_customer",
            addr_line_1="abc",
            addr_line_2="xyz",
            city="aaa",
            state="bbb",
            uuid="b73a7a28"  #Specific UUID for testing of Order Endpoint
        ),
        "delete_customer": Customer(
            email="delete@example.com",
            password="$2b$12$S/g71WXkT3QK1GOdIXHjc.cHudJ/m62nBga0t91xikWRh7gQ/ni3.",  #Hashed password
            name="delete",
            addr_line_1="abc",
            addr_line_2="xyz",
            city="aaa",
            state="bbb",
            uuid="2b203687"  #Specific UUID for testing of Order Endpoint
        )
    }
    return data
