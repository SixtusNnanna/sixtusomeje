from pydantic import BaseModel
from fastapi.security.oauth2 import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/auth/token")


class TokenData(BaseModel):
    access_token: str
    token_type: str
