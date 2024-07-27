from datetime import datetime
from pydantic import BaseModel


class CustomerBase(BaseModel):
    email: str
    name: str
    addr_line_1: str
    addr_line_2: str
    city: str
    state: str

class CustomerCreate(CustomerBase):
    password: str

class Customer(CustomerBase):
    id: int
    is_verified: bool
    creation_date: datetime
    uuid: str

    class Config:
        orm_mode = True
