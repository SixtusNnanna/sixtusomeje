from fastapi import APIRouter, HTTPException, status
from app.api.dependencies import OrderDeps, CurrentUserDeps
from app.api.schemas.order import OrderCreate, OrderRead


router = APIRouter()


@router.post("/", response_model=OrderRead, status_code=201)
async def order_create(service: OrderDeps, user: CurrentUserDeps, order_data: OrderCreate):
    new_order = await service.create_order(order_create=order_data)
    return new_order


@router.get("/", status_code=200)
async def complete_order(order_id: int, service: OrderDeps, user: CurrentUserDeps):
    order_complete = await service.complete_order(order_id=order_id)
    if not order_complete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order Not Found or Already Completed"
        )
    return order_complete

