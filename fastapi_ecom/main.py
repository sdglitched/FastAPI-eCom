from fastapi import FastAPI

from fastapi_ecom.router import customer


app = FastAPI(
        title="FastAPI ECOM",
        description="E-Commerce API for businesses and end users using FastAPI.",
        version="0.1.0"
    )

@app.get("/")
def root():
    return{"message": "This is an E-Commerce API for businesses and end users using FastAPI."}

app.include_router(customer.router)
