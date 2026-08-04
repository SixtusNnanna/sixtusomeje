from app.databaase.models import Order, OrderItem
from app.api.schemas.order import OrderCreate
from app.api.schemas.order_item import OrderItemCreate
from app.services.base import BaseService
from app.services.inventory import InventoryService
from app.core.enum import OrderStatus


class OrderService(BaseService[Order]):
    def __init__(self, session):
        super().__init__(session, Order)
        self.inventory = InventoryService
