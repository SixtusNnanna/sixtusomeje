from sqlalchemy.ext.asyncio import AsyncSession
from app.databaase.models import Customer
from app.services.base import BaseService
from app.api.schemas.customer import CustomerCreate, CustomerUpdate
from app.exceptions import NotFoundExcept


class CustomerService(BaseService[Customer]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Customer)

    async def get_customer_id(self, id: int):
        cusotmer = await self.get(id)
        if cusotmer is None:
            raise NotFoundExcept("Customer")

    async def add_customer(self, cusotmer_data: CustomerCreate):
        new_customer = Customer(
            **cusotmer_data.model_dump()
        )
        return await self.add(new_customer)

    async def update_customer(self, customer_id: int,  update_data: CustomerUpdate):
        updates = update_data.model_dump()
        return await self.update({"id": customer_id}, updates)

    async def delete_customer(self, customer_id: int):
        customer = await self.get_customer_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with ID {customer_id} does not exist.")
        return await self.delete(id=customer_id)






