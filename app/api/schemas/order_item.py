from decimal import Decimal
from pydantic import BaseModel


class OrderItemBase(BaseModel):
    product_id: int
    order_id: int
    quantity: int
    unit_price: Decimal


class OrderItemCreate(OrderItemBase):
    product_id: int
    order_id: int
    quantity: int
    unit_price: Decimal


class OrderItemResponse(OrderItemBase):
    id: int

    class Config:
        orm_mode = True



