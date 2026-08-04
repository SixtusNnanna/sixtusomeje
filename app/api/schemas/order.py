from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class OrderBase(BaseModel):
    customer_id: int
    order_date: datetime
    selling_price: Decimal


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int
