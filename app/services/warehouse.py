from sqlalchemy.ext.asyncio import AsyncSession
from app.databaase.models import Warehouse
from app.services.base import BaseService
from app.api.schemas.warehouse import WarehouseCreate, WarehouseUpdate


class WareHouseService(BaseService[Warehouse]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Warehouse)

    async def list_warehouse(
            self,
            offset: int,
            limit: int
    ):
        return await self.list(offset, limit)

    async def add_warehouse(self, warehouse_data: WarehouseCreate):
        new_warehouse = Warehouse(
            **warehouse_data.model_dump()
        )
        return await self.add(new_warehouse)

    async def get_warehouse(self, warehouse_id: int):
        return await self.get(warehouse_id)

    async def warehouse_update(self, warehouse_id: int, update_data: WarehouseUpdate):
        updates = update_data.model_dump()
        return await self.update({"id": warehouse_id}, updates)

    async def delete_warehouse(self, warehouse_id: int):
        warehouse = self.get_warehouse(warehouse_id=warehouse_id)
        if warehouse is None:
            raise ValueError("Warehouse Does not exisit")
        return await self.delete(id=warehouse_id)

