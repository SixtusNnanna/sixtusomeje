from fastapi import APIRouter

from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.products import router as product_router
from app.api.v1.endpoints.customer import router as customer_router


router = APIRouter()
router.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
router.include_router(product_router, prefix="/api/v1/products", tags=["Products"])
router.include_router(customer_router, prefix="/api/v1/customers", tags=["Customer"])
