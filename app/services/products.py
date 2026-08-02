from app.services.base import BaseService
from app.databaase.models import Product
from app.api.schemas.product import ProductCreate, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.utlis import generate_sku


class ProductService(BaseService[Product]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Product)

    async def get_product(self, product_id: int) -> Product | None:
        return await self.get(id=product_id)

    async def list_products(self, offset: int, limit: int, ) -> list[Product]:
        return await self.list(offset_val=offset, limit_val=limit)

    async def create_product(self, product_data: ProductCreate) -> Product:
        sku = generate_sku(product_data.name)
        new_product = Product(sku=sku, **product_data.model_dump(exclude={"sku"}))
        return await self.add(new_product)

    async def update_product(
        self, product_id: int, product_data: ProductUpdate
    ) -> Product | None:
        updates = product_data.model_dump(exclude_unset=True)
        return await self.update({"id": product_id}, updates)

    async def delete_product(self, product_id: int) -> bool:
        product = await self.get_product(product_id=product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} does not exist.")
        return await self.delete(id=product_id)
