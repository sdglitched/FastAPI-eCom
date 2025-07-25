import uvicorn
from fastapi import FastAPI

from fastapi_ecom.config import config
from fastapi_ecom.router import business, customer, order, product

# Metadata for API tags
tags_metadata = [
    {"name": "business", "description": "Operations on businesses"},
    {"name": "product", "description": "Operations on products"},
    {"name": "customer", "description": "Operations on customers"},
    {"name": "order", "description": "Operations on orders"}
]

# Initialize the FastAPI application
app = FastAPI(
        title="FastAPI ECOM",
        description="E-Commerce API for businesses and end users using FastAPI.",
        version="0.1.0",
        openapi_tags=tags_metadata,
    )

PREFIX = "/api/v1"

@app.get("/")
def root() -> dict[str, str]:
    """
    Root endpoint of the FastAPI application.

    :return: Metadata about the API, including title, description, and version.
    """
    return{
        "title": "FastAPI ECOM",
        "description": "E-Commerce API for businesses and end users using FastAPI.",
        "version": "0.1.0"
    }

# Include routers for different modules
app.include_router(business.router, prefix=PREFIX)
app.include_router(product.router, prefix=PREFIX)
app.include_router(customer.router, prefix=PREFIX)
app.include_router(order.router, prefix=PREFIX)


def start_service():
    """
    Start the FastAPI application.

    This function configures and runs the Uvicorn server using settings from the application
    configuration.

    :raises RuntimeError: If configuration parameters are missing or invalid.
    """
    uvicorn.run(
        "fastapi_ecom.app:app",
        host=config.servhost,
        port=config.servport,
        reload=config.cgreload,
    )
