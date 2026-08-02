from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    staff = "staff"


class ProductStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class OrderStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
