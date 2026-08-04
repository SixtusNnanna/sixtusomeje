from typing import  Optional
from pydantic import BaseModel, Field, ConfigDict
from app.core.enum import ProductStatus
from decimal import Decimal

class ProductBase(BaseModel):
    name: str = Field(..., example="Product Name")
    description: str = Field(..., example="Product Description")
    unit_price: Decimal = Field(..., example=9.99, gt=0)


class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    unit_price: Decimal | None = None
    sku: str | None = None


class ProductResponse(ProductBase):
    id: int
    sku: str
    status: ProductStatus

    model_config = ConfigDict(from_attributes=True)
