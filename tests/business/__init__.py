from typing import Dict
from uuid import uuid4

from fastapi_ecom.database.models.business import Business


def _test_data_business() -> Dict[str, Business]:
    """
    Provides test data for testing the business endpoint.

    :return: A dictionary containing Business objects for testing.
    """
    data = {
        "test_business": Business(
            email="test_business@example.com",
            password="test_business",
            name="test_business",
            addr_line_1="abc",
            addr_line_2="xyz",
            city="aaa",
            state="bbb",
            uuid=uuid4().hex[0:8]
        ),
        "duplicate_business": Business(
            email="duplicate_business@example.com",
            password="duplicate_business",
            name="duplicate_business",
            addr_line_1="abc",
            addr_line_2="xyz",
            city="aaa",
            state="bbb",
            uuid=uuid4().hex[0:8]
        ),
        "delete_business": Business(
            email="delete@example.com",
            password="$2b$12$S/g71WXkT3QK1GOdIXHjc.cHudJ/m62nBga0t91xikWRh7gQ/ni3.",  #Hashed password
            name="delete",
            addr_line_1="abc",
            addr_line_2="xyz",
            city="aaa",
            state="bbb",
            uuid=uuid4().hex[0:8]
        )
    }
    return data
