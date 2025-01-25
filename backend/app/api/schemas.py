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


class PartVariantSchema(BaseSchema):
    """
    Schema for representing a part variant.
    """

    part_id: UUID
    name: str
    price: float


class PartVariantCreateSchema(BaseModel):
    """
    Schema for creating a part variant.
    """

    part_id: UUID
    name: str
    price: float


class PartVariantUpdateSchema(BaseModel):
    """
    Schema for updating a part variant (all fields optional).
    """

    part_id: Optional[UUID] = None
    name: Optional[str] = None
    price: Optional[float] = None


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


class ProductUpdateSchema(BaseModel):
    """
    Schema for updating a product (all fields optional).
    """

    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    base_price: Optional[float] = None
    is_custom: Optional[bool] = None
