from typing import  Optional
from pydantic import BaseModel, Field, ConfigDict


class WarehouseBase(BaseModel):
    name: str = Field(..., example="Warehouse Name")
    address: str = Field(..., example="Warehouse Address")
    manager_name: str = Field(..., example="Manager Name")


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    manager_name: str | None = None


class WarehouseResponse(WarehouseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
