from sqlalchemy import Integer, String, Boolean, ForeignKey, UniqueConstraint, Numeric, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Enum as SqlEnum
from app.databaase.base import Base
from app.core.enum import Role, ProductStatus, OrderStatus
from decimal import Decimal


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    role: Mapped[Role] = mapped_column(SqlEnum(Role), default=Role.staff)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    orders: Mapped[list["Order"]] = relationship(
        "Order", back_populates="customer", cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sku: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(String)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[ProductStatus] = mapped_column(
        SqlEnum(ProductStatus), default=ProductStatus.ACTIVE
    )
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")
    inventories: Mapped[list["Inventory"]] = relationship(back_populates="product")


class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    address: Mapped[str] = mapped_column(String)
    manager_name: Mapped[str] = mapped_column(String)
    inventories: Mapped[list["Inventory"]] = relationship(back_populates="warehouse")


class OrderItemAllocation(Base):
    __tablename__ = "order_item_allocations"
    __table_args__ =(
        UniqueConstraint("order_item_id", "warehouse_id", name="uq_order_item_warehouse"),
        CheckConstraint("quantity > 0", name="ck_allocation_quantity_positive"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_item_id = mapped_column(Integer, ForeignKey("order_items.id"))
    warehouse_id = mapped_column(Integer, ForeignKey("warehouses.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    order_item: Mapped["OrderItem"] = relationship(back_populates="allocations")
    warehouse: Mapped["Warehouse"] = relationship()

class Inventory(Base):
    __tablename__ = "inventories"
    __table_args__ = (UniqueConstraint("warehouse_id", "product_id", name="uq_warehouse_product"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id"), index=True
    )
    warehouse_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("warehouses.id"), index=True
    )
    quantity: Mapped[int] = mapped_column(Integer)
    minimum_stock_level: Mapped[int] = mapped_column(Integer)
    product: Mapped["Product"] = relationship(back_populates="inventories")
    warehouse: Mapped["Warehouse"] = relationship(back_populates="inventories")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.id"), index=True
    )
    order_date: Mapped[str] = mapped_column(String)
    selling_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[OrderStatus] = mapped_column(
        SqlEnum(OrderStatus), default=OrderStatus.PENDING
    )
    customer: Mapped["Customer"] = relationship(back_populates="orders")
    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan",
        lazy="selectin"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), index=True)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id"), index=True
    )
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    order: Mapped["Order"] = relationship(back_populates="order_items")
    product: Mapped["Product"] = relationship(back_populates="order_items", lazy="selectin")
    allocations: Mapped["OrderItemAllocation"] = relationship(back_populates="order_item")
