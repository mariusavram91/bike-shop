# app/api/schemas.py

from uuid import UUID
from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel


class BaseSchema(BaseModel):
    """
    Base schema that includes common fields for all schemas.

    Attributes:
        id (UUID): Unique identifier for the model.
        created_at (datetime): The timestamp when the model was created.
        updated_at (datetime): The timestamp when the model was last
            updated.
    """

    id: UUID
    created_at: datetime
    updated_at: datetime


class CartItemSchema(BaseSchema):
    """
    Schema for representing an item in a shopping cart.
    """

    cart_id: Optional[UUID] = None
    product_id: UUID
    selected_parts: Optional[str] = None
    total_price: float


class CartItemCreateSchema(BaseModel):
    """
    Schema for creating an item in a shopping cart.
    """

    cart_id: Optional[UUID] = None
    product_id: UUID
    selected_parts: Optional[str] = None
    total_price: float


class CartItemUpdateSchema(BaseModel):
    """
    Schema for updating an item in a shopping cart (all fields optional).
    """

    cart_id: Optional[UUID] = None
    product_id: Optional[UUID] = None
    selected_parts: Optional[str] = None
    total_price: Optional[float] = None


class CartSchema(BaseSchema):
    """
    Schema for representing a shopping cart.
    """

    purchased: bool
    total_price: float

    items: Optional[List[CartItemSchema]] = []


class CartCreateSchema(BaseModel):
    """
    Schema for creating a shopping cart.
    """

    purchased: bool
    total_price: float

    items: List[CartItemCreateSchema]


class CartUpdateSchema(BaseModel):
    """
    Schema for updating a shopping cart (all fields optional).
    """

    purchased: Optional[bool] = None
    total_price: Optional[float] = None


class VariantDependencySchema(BaseModel):
    """
    Schema for representing a dependency between part variants.
    """

    variant_id: UUID
    restrictions: Optional[str] = None


class VariantDependencyCreateSchema(BaseModel):
    """
    Schema for creating a dependency between part variants.
    """

    variant_id: UUID
    restrictions: Optional[str] = None


class VariantDependencyUpdateSchema(BaseModel):
    """
    Schema for updating a dependency between part variants.
    """

    variant_id: Optional[UUID] = None
    restrictions: Optional[str] = None


class PartVariantSchema(BaseSchema):
    """
    Schema for representing a part variant.
    """

    part_id: UUID
    name: str
    price: float
    is_available: bool
    stock_quantity: int

    dependencies: Optional[List[VariantDependencySchema]] = []


class PartVariantCreateSchema(BaseModel):
    """
    Schema for creating a part variant.
    """

    part_id: UUID
    name: str
    price: float
    is_available: bool
    stock_quantity: int


class PartVariantUpdateSchema(BaseModel):
    """
    Schema for updating a part variant (all fields optional).
    """

    part_id: Optional[UUID] = None
    name: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    stock_quantity: Optional[int] = None


class ProductPartSchema(BaseSchema):
    """
    Schema for representing a product part.
    """

    product_id: UUID
    name: str

    variants: Optional[List[PartVariantSchema]] = []


class ProductPartCreateSchema(BaseModel):
    """
    Schema for creating a product part.
    """

    product_id: UUID
    name: str


class ProductPartUpdateSchema(BaseModel):
    """
    Schema for updating a product part (all fields optional).
    """

    product_id: Optional[UUID] = None
    name: Optional[str] = None


class ProductSchema(BaseSchema):
    """
    Schema for representing a product.
    """

    name: str
    description: Optional[str] = None
    category: str
    base_price: float
    is_custom: bool
    is_available: bool
    stock_quantity: int

    parts: Optional[List[ProductPartSchema]] = []


class ProductCreateSchema(BaseModel):
    """
    Schema for creating a new product.
    """

    name: str
    description: Optional[str] = None
    category: str
    base_price: float
    is_custom: bool
    is_available: bool
    stock_quantity: int


class ProductUpdateSchema(BaseModel):
    """
    Schema for updating a product (all fields optional).
    """

    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    base_price: Optional[float] = None
    is_custom: Optional[bool] = None
    is_available: Optional[bool] = None
    stock_quantity: Optional[int] = None
