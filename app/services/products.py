from app.services.base import BaseService
from app.databaase.models import Product
from app.api.schemas.product import ProductCreate, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.utlis import generate_sku
from app.exceptions import NotFoundExcept, ExistException

class ProductService(BaseService[Product]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Product)

    async def get_product(self, product_id: int) -> Product | None:
        product = await self.get(id=product_id)
        if not product:
            raise NotFoundExcept("Product")
        return product

    async def list_products(self, offset: int, limit: int, ) -> list[Product]:
        return await self.list(offset_val=offset, limit_val=limit)

    async def create_product(self, product_data: ProductCreate) -> Product:
        existing_product = await self.get_item(name=product_data.name)
        if existing_product:
            raise ExistException(existing_product.name)
        sku = generate_sku(product_data.name)
        new_product = Product(sku=sku, **product_data.model_dump())
        return await self.add(new_product)

    async def update_product(
        self, product_id: int, product_data: ProductUpdate
    ) -> Product | None:
        prod = await self.get_product(product_id)
        if prod is None:
            raise NotFoundExcept("Product")
        updates = product_data.model_dump(exclude_unset=True)

        return await self.update({"id": product_id}, updates)

    async def delete_product(self, product_id: int) -> bool:
        product = await self.get_product(product_id=product_id)
        if not product:
            raise NotFoundExcept("Product")
        return await self.delete(id=product_id)
