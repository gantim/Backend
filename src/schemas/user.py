from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserBaseSchema(BaseModel):
    first_name: str
    middle_surname: str
    surname: str
    phone: str
    address: str
    bonus: int = None
    email: EmailStr
    role: str


class CreateUserSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")


class UserSchema(UserBaseSchema):
    id: int
    is_active: Optional[bool] = Field(default=False)

    class Config:
        orm_mode = True


class UserOutSchema(BaseModel):
    id: int
    first_name: str
    middle_surname: str
    surname: str
    phone: str
    address: str
    bonus: int = None
    email: EmailStr
    role: str

    class Config:
        orm_mode = True