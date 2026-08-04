from pydantic import BaseModel, Field, ConfigDict


class InventoryBase(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int = Field(gt=0)
    minimum_stock_level: int


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int | None = Field(gt=0, default=None)
    minimum_stock_level: int | None = None


class InventoryResponse(InventoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class StockRequest(BaseModel):
    warehouse_id: int
    product_id: int
    quantity: int


class TransferRequest(BaseModel):
    source_warehouse_id: int
    destination_warehouse_id: int
    product_id: int
    quantity: int






