from fastapi import APIRouter, HTTPException, status

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

    product = await service.get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"

        )
    return product


@router.post("/", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    service: ProductServiceDeps,
    current_user: CurrentUserDeps
):
    new_product = await service.create_product(product_data)
    return new_product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    service: ProductServiceDeps,
    current_user: CurrentUserDeps
):
    return await service.update_product(product_id, product_data)


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    service: ProductServiceDeps,
    current_user: CurrentUserDeps
):
    res = await service.delete_product(product_id)
    if not res:
        return {"detail": "Product not found"}
    return {"detail": "Product deleted successfully"}

