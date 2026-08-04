from app.databaase.models import Order, OrderItem, OrderItemAllocation
from app.api.schemas.order import OrderCreate, OrderItemCreate
from app.services.base import BaseService
from app.services.inventory import InventoryService
from app.core.enum import OrderStatus
from decimal import Decimal


class OrderService(BaseService[Order]):
    def __init__(self, session, inventory: InventoryService):
        super().__init__(session, Order)
        self.inventory = inventory

    async def create_order(self, order_create: OrderCreate):
        selling_price = Decimal(0)
        order = Order(
            customer_id=order_create.customer_id,
            order_date=order_create.order_date,
            status=OrderStatus.PENDING,
            selling_price=1

        )
        self.session.add(order)
        await self.session.flush()

        for item in order_create.order_items:
            item_total = item.unit_price * item.quantity
            selling_price += item_total

            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price
            )

        self.session.add(order_item)

        order.selling_price = selling_price

        await self.session.commit()
        await self.session.refresh(order, attribute_names=["order_items"])
        return order

    async def complete_order(self, order_id: int):
        order = await self.get(id=order_id)
        if order is None:
            raise ValueError("Order is not Found")
        if order.status != OrderStatus.PENDING:
            raise ValueError("Cannot continue this order")
        for item in order.order_items:
            allocations = await self.inventory.allocate_stock(
                item.product_id, item.quantity
                )
            for warehouse_id, qty in allocations:
                self.session.add(
                    OrderItemAllocation(
                        order_item_id=item.id,
                        warehouse_id=warehouse_id,
                        quantity=qty
                        )
                    )
        order.status = OrderStatus.COMPLETED

        await self.session.commit()
        await self.session.refresh(order)
        return order
