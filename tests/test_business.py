import pytest


@pytest.mark.parametrize(
    "data",
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
            id="BUSINESS Endpoint - 201 Created",
        )
    ]
)
async def test_create_business(client, data):
    response = await client.post("/api/v1/business/create", json = data)
    print("testfunc... IDHR PAHUCH GYA")
    print(response.json())
    assert response.status_code == 201
