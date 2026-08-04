from sqlalchemy import select
from app.databaase.models import Inventory
from app.api.schemas.inventory import InventoryCreate
from app.services.base import BaseService
from app.exceptions import NotFoundExcept, ExistException,NotZeroError, SameWareHouseTransferError, InSufficentStockError


class InventoryService(BaseService[Inventory]):
    def __init__(self, session):
        super().__init__(session, Inventory)

    async def get_inventories_of_product(self, product_id):
        inventory = await self.list(product_id=product_id)
        if not inventory:
            raise NotFoundExcept("Inventory")
        return inventory

    async def list_inventory(self, offset: int, limit: int):
        return await self.list(offset_val=offset, limit_val=limit)

    async def create_inventory(self, inventory_data: InventoryCreate):
        existing_inventory = await self.get_item(
            product_id=inventory_data.product_id,
            warehouse_id=inventory_data.warehouse_id
        )
        if existing_inventory:
            raise ExistException(
                "Inventory"
            )
        new_inventory = Inventory(**inventory_data.model_dump())
        return await self.add(new_inventory)

    async def get_inventory(self, product_id: int, warehouse_id: int):
        result = await self.get_item(product_id=product_id, warehouse_id=warehouse_id)
        if result is None:
            raise NotFoundExcept(
                "Inventory"
            )
        return result

    async def increase_stock(self, warehouse_id, product_id, quantity):
        if quantity <= 0:
            raise NotZeroError
        inventory = await self.get_inventory(product_id, warehouse_id)

        if not inventory:
            inventory = Inventory(
                warehouse_id=warehouse_id,
                product_id=product_id,
                quantity=0,
            )
            await self.add(inventory)

        inventory.quantity += quantity
        await self.session.commit()
        await self.session.refresh(inventory)
        return inventory

    async def reduce_stock(
            self, warehouse_id: int, product_id: int, quantity: int
            ):
        if quantity <= 0:
            raise NotZeroError

        inventory = await self.get_inventory(product_id, warehouse_id)
        if not inventory:
            raise NotFoundExcept("Inventory")
        inventory.quantity -= quantity
        await self.session.commit()
        await self.session.refresh(inventory)
        return inventory

    async def transfer_stock(
            self,
            source_warehouse_id: int,
            destination_warehouse_id: int,
            product_id: int,
            quantity
            ):
        if source_warehouse_id == destination_warehouse_id:
            raise SameWareHouseTransferError

        source = await self.get_inventory(product_id, source_warehouse_id)

        if not source:
            raise NotFoundExcept("Source")

        if source.quantity < quantity:
            raise InSufficentStockError

        destination = await self.get_inventory(
            product_id, destination_warehouse_id
        )
        source.quantity -= quantity

        if destination:
            destination.quantity += quantity
        else:
            destination = Inventory(
                warehouse_id=destination_warehouse_id,
                product_id=product_id,
                quantity=quantity,
                minimum_stock_level=10
            )
            self.session.add(destination)

        await self.session.commit()
        return {
            "message": "Stock transferred successfully"
        }

    async def get_lockable_stock_for_product(
        self, product_id: int
    ) -> list[Inventory]:
        stmt = (
            select(Inventory)
            .where(
                Inventory.product_id == product_id,
                Inventory.quantity > 0,
            )
            .order_by(Inventory.quantity.desc())
            .with_for_update()
        )

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def allocate_stock(
        self, product_id: int, quantity_needed: int
    ) -> list[tuple[int, int]]:
        candidates = await self.get_lockable_stock_for_product(product_id)

        total_available = sum(inv.quantity for inv in candidates)
        if total_available < quantity_needed:
            raise InSufficentStockError

        allocations: list[tuple[int, int]] = []
        remaining = quantity_needed
        for inv in candidates:
            if remaining <= 0:
                break
            take = min(inv.quantity, remaining)
            inv.quantity -= take
            allocations.append((inv.warehouse_id, take))
            remaining -= take

        return allocations









