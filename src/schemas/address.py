from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class AddressBaseSchema(BaseModel):
    address: str
    id_user: int
    apartment_number: int
    entrance: str
    floor: int
    doorphone: str


class AddressSchema(AddressBaseSchema):
    id: int
    id_user: int

    class Config:
        orm_mode = True