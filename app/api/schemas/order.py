from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
from .product import ProductResponse
from app.core.enum import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: Decimal

    @field_validator("quantity")
    @classmethod
    def quantity_postive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than Zero")
        return v


class OrderBase(BaseModel):
    customer_id: int
    order_date: str



class OrderCreate(OrderBase):
    order_items: list[OrderItemCreate] = Field(min_length=1)

    @field_validator("order_items")
    @classmethod
    def items_not_empty(cls, v: list[OrderItemCreate]):
        if not v:
            raise ValueError("Order must contain at least one item")
        return v


class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    product: ProductResponse


class OrderRead(OrderBase):
    id: int
    customer_id: int
    status: OrderStatus
    order_date: str
    # order_items: list[OrderItemRead]
    selling_price: Decimal
