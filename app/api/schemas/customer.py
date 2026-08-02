from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class CustomerBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: PhoneNumber


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    phone_number: PhoneNumber | None = None


class CustomerResponse(CustomerBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
