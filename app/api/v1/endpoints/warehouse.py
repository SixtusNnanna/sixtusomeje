from fastapi import APIRouter, HTTPException, status
from app.api.dependencies import WareHouseServicesDeps, CurrentUserDeps
from app.api.schemas.warehouse import WarehouseUpdate, WarehouseCreate, WarehouseResponse


router = APIRouter()


@router.get("/", response_model=list[WarehouseResponse], status_code=200)
async def get_list_warehouse(service: WareHouseServicesDeps, offset: int = 0, limit: int = 0):
    return await service.list_warehouse(offset, limit)


@router.post("/", response_model=WarehouseResponse)
async def add_warehouse(service: WareHouseServicesDeps, create_data: WarehouseCreate, user: CurrentUserDeps):
    return await service.add_warehouse(warehouse_data=create_data)


@router.put("/{warehouse_id}", response_model=WarehouseResponse, status_code=200)
async def update_warehouse(warehouse_id: int, service: WareHouseServicesDeps, update_data: WarehouseUpdate, user: CurrentUserDeps):
    return await service.warehouse_update(warehouse_id, update_data)


@router.delete("/{warehouse_id}/", status_code=204)
async def warehouse_delete(warehouse_id: int, service: WareHouseServicesDeps, user: CurrentUserDeps):
    result = await service.delete_warehouse(warehouse_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Not Found"
        )
    return {
        "message": "Warehouse Deleted Successfully"
    }
