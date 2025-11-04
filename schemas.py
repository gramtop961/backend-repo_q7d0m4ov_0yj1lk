"""
Database Schemas for Bits&Bites Restaurant App

Each Pydantic model represents a MongoDB collection. The collection name
is the lowercase of the class name (e.g., Order -> "order").
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class Product(BaseModel):
    """Menu product schema (for reference/validation)
    Collection name: "product"
    """
    name: str = Field(..., description="Product name")
    price: float = Field(..., ge=0, description="Price in currency units")
    category: str = Field(..., description="Menu category, e.g., Dosa, Rolls")
    available: bool = Field(True, description="Whether the item is currently available")


class OrderItem(BaseModel):
    name: str
    price: float
    quantity: int = Field(1, ge=1)


class Order(BaseModel):
    """Customer order schema
    Collection name: "order"
    """
    customer_name: str = Field(..., description="Customer full name")
    contact_number: str = Field(..., description="Phone number")
    payment_method: str = Field(..., description="One of: COD, UPI")
    items: List[OrderItem] = Field(..., description="Items in the order")
    subtotal: float = Field(..., ge=0)
    discount: float = Field(0, ge=0, description="Discount applied (offers/coupons)")
    total: float = Field(..., ge=0)
    notes: Optional[str] = Field(None, description="Optional notes")
    status: str = Field("placed", description="Order status")
