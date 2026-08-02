from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import CurrentUserDeps, CustomerServiceDeps
from app.api.schemas.customer import CustomerResponse, CustomerCreate, CustomerUpdate


router = APIRouter()


@router.get("/{customer_id}", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
async def get_customers(customer_id: int, service: CustomerServiceDeps, user: CurrentUserDeps):
    return await service.get_customer_id(customer_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CustomerResponse)
async def create_customer(
    customer_data: CustomerCreate,
    service: CustomerServiceDeps,
    user: CurrentUserDeps
    ):
    return await service.add_customer(customer_data)


@router.put("/{customer_id}/update", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
async def udate_customer(
    customer_id: int,
    update_data: CustomerUpdate,
    service: CustomerServiceDeps,
    user: CurrentUserDeps
    ):
    return await service.update_customer(customer_id=customer_id, update_data=update_data)


@router.delete("/{customer_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def customer_delete(
    customer_id: int,
    service: CustomerServiceDeps,
    user: CurrentUserDeps
    ):
    result = await service.delete_customer(customer_id=customer_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer you are about to delete is not boarded"
        )




