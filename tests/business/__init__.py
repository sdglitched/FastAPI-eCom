from fastapi_ecom.database.models.business import Business


def _test_data_business() -> dict[str, Business]:
    """
    Provides test data for testing the business endpoint.

    :return: A dictionary containing Business objects for testing.
    """
    data = {
        "test_business": Business(
            email="test_business@example.com",
            password="$2b$12$cV19rR.8VjQwJW3s/NtSv.AYjXPN9FaK/DZXItCpylBeCRpsBVF9.",  #Hashed password
            name="test_business",
            addr_line_1="abc",
            addr_line_2="xyz",
            city="aaa",
            state="bbb",
            uuid="d76a11f2"  #Specific UUID for testing of Product Endpoint
        ),
        "duplicate_business": Business(
            email="duplicate_business@example.com",
            password="$2b$12$4M6sS/Fk13etEBHOkb7fD.ors5LAQxyOtSC2p2ST53EnmyPFDoE0O",    #Hashed password
            name="duplicate_business",
            addr_line_1="abc",
            addr_line_2="xyz",
            city="aaa",
            state="bbb",
            uuid="fd4a8cac"  #Specific UUID for testing of Product Endpoint
        ),
        "delete_business": Business(
            email="delete@example.com",
            password="$2b$12$S/g71WXkT3QK1GOdIXHjc.cHudJ/m62nBga0t91xikWRh7gQ/ni3.",  #Hashed password
            name="delete",
            addr_line_1="abc",
            addr_line_2="xyz",
            city="aaa",
            state="bbb",
            uuid="5c1c48fb"  #Specific UUID for testing of Product Endpoint
        )
    }
    return data
