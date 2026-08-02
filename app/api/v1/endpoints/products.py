from fastapi import APIRouter

from app.api.dependencies import CurrentUserDeps, ProductServiceDeps
from app.api.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter()


@router.get("/", response_model=list[ProductResponse])
async def list_products(
    service: ProductServiceDeps,
    current_user: CurrentUserDeps
):
    return await service.list()


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    service: ProductServiceDeps,
    current_user: CurrentUserDeps
):
    return await service.get(product_id)


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product_data: ProductCreate,
    service: ProductServiceDeps,
    current_user: CurrentUserDeps
):
    return await service.create_product(product_data)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    service: ProductServiceDeps,
    current_user: CurrentUserDeps
):
    return await service.update_product(product_id, product_data)


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    service: ProductServiceDeps,
    current_user: CurrentUserDeps
):
    res = await service.delete_product(product_id)
    if not res:
        return {"detail": "Product not found"}
    return {"detail": "Product deleted successfully"}

