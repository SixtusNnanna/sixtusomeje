import re
import secrets
from datetime import date
from enum import Enum

from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.config import app_settings as settings


def generate_sku(name: str, created_on: date | None = None) -> str:
    created_on = created_on or date.today()
    name_part = re.sub(r"[^A-Za-z0-9]", "", name).upper()[:12]
    date_part = created_on.strftime("%Y%m%d")
    suffix = secrets.token_hex(1).upper()  # 2 hex chars
    return f"{name_part}-{date_part}-{suffix}"


class Period(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


def create_access_token(payload: dict, expiry: timedelta | None = None):
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + \
        (expiry or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token=token, key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expires access token")





