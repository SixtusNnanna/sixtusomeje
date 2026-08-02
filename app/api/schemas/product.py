from typing import  Optional
from pydantic import BaseModel, Field
from app.core.enum import ProductStatus

class ProductBase(BaseModel):
    name: str = Field(..., example="Product Name")
    description: str = Field(..., example="Product Description")
    unit_price: float = Field(..., example=9.99)


class ProductCreate(ProductBase):
    sku: str = Field(..., example="SKU12345")

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    unit_price: float | None = None
    sku: str | None = None


class ProductResponse(ProductBase):
    id: int
    sku: str
    status: ProductStatus

    class Config:
        orm_mode = True
