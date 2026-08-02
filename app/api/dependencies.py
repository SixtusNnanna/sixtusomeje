from typing import Annotated
from jose import JWTError
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.databaase.session import get_async_session
from app.services.user import UserService
from app.databaase.models import User
from app.core.security import oauth2_scheme
from app.utlis import decode_access_token
from app.services.products import ProductService
from app.services.customer import CustomerService


SessionDps = Annotated[AsyncSession, Depends(get_async_session)]


def get_user_service(session: SessionDps) -> UserService:
    return UserService(session=session)


UserDeps = Annotated[User, Depends(get_user_service)]

def get_product_service(session: SessionDps) -> ProductService:
    return ProductService(session=session)

def get_token_data(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = decode_access_token(token)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Token"
        )


async def get_current_user(
    payload: Annotated[dict, Depends(get_token_data)],
    service: UserDeps
):
    user_id = payload.get("id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired"
        )
    user = await service.get(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

CurrentUserDeps = Annotated[User, Depends(get_current_user)]

ProductServiceDeps = Annotated[ProductService, Depends(get_product_service)]


async def get_admin_user(
    current_user: CurrentUserDeps
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )
    return current_user

AdminUserDeps = Annotated[User, Depends(get_admin_user)]


def get_cusomter_service(session: SessionDps) -> CustomerService:
    return CustomerService(session=session)


CustomerServiceDeps = Annotated[CustomerService, Depends(get_cusomter_service)]


