from fastapi import FastAPI

from fastapi_ecom.router import business, customer, order, product

tags_metadata = [
    {"name": "customer", "description": "Operations on customeres"},
    {"name": "business", "description": "Operations on businesses"},
    {"name": "product", "description": "Operations on products"},
    {"name": "order", "description": "Operations on orders"}
]

app = FastAPI(
        title="FastAPI ECOM",
        description="E-Commerce API for businesses and end users using FastAPI.",
        version="0.1.0",
        openapi_tags=tags_metadata,
    )

PREFIX = "/api/v1"

@app.get("/")
def root():
    return{"message": "This is an E-Commerce API for businesses and end users using FastAPI."}

app.include_router(customer.router, prefix=PREFIX)
app.include_router(business.router, prefix=PREFIX)
app.include_router(product.router, prefix=PREFIX)
app.include_router(order.router, prefix=PREFIX)
