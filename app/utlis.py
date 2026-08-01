import re
import secrets
from datetime import date

def generate_sku(name: str, created_on: date | None = None) -> str:
    created_on = created_on or date.today()
    name_part = re.sub(r"[^A-Za-z0-9]", "", name).upper()[:12]
    date_part = created_on.strftime("%Y%m%d")
    suffix = secrets.token_hex(1).upper()  # 2 hex chars
    return f"{name_part}-{date_part}-{suffix}"
