from fastapi import APIRouter
from app.api.schemas.inventory import InventoryCreate, InventoryResponse, StockRequest, TransferRequest
from app.api.dependencies import InventoryDeps, CurrentUserDeps


router = APIRouter()


@router.get("/", response_model=list[InventoryResponse])
async def inventory_list(offset: int, limit: int, service: InventoryDeps, user: CurrentUserDeps):
    return await service.list_inventory(offset, limit)


@router.get("/{inventory_id}/", response_model=InventoryResponse)
async def get_inventory(
    inventory_id: int,
    service: InventoryDeps,
    user: CurrentUserDeps,
):
    return await service.get(inventory_id)


@router.post("/", response_model=InventoryResponse)
async def inventory_create(
    service: InventoryDeps,
    inventory_data: InventoryCreate,
    user: CurrentUserDeps,
):
    return await service.create_inventory(inventory_data)


@router.post("/inventory/increase")
async def increase_stock(
    data: StockRequest,
    service: InventoryDeps,
    user: CurrentUserDeps,
):
    return await service.increase_stock(
        warehouse_id=data.warehouse_id,
        product_id=data.product_id,
        quantity=data.quantity
    )


@router.post("/inventory/reduce")
async def reduce_stock(
    data: StockRequest,
    service: InventoryDeps,
    user: CurrentUserDeps,
):
    return await service.reduce_stock(
        warehouse_id=data.warehouse_id,
        product_id=data.product_id,
        quantity=data.quantity
    )


@router.post("/inventory/transfer")
async def transfer_stock(
    data: TransferRequest,
    service: InventoryDeps,
    user: CurrentUserDeps
):
    return await service.transfer_stock(
        source_warehouse_id=data.source_warehouse_id,
        destination_warehouse_id=data.destination_warehouse_id,
        product_id=data.product_id,
        quantity=data.quantity
    )






