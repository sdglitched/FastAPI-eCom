async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "title": "FastAPI ECOM",
        "description": "E-Commerce API for businesses and end users using FastAPI.",
        "version": "0.1.0"
    }
