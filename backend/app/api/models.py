# app/api/models.py

from uuid import UUID, uuid4
from typing import Optional, List
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel, Relationship


class BaseModel(SQLModel):
    """
    Base model that includes common fields for all database models.

    Attributes:
        id (UUID): Unique identifier for the model.
        created_at (datetime): The timestamp when the model was created.
        updated_at (datetime): The timestamp when the model was last
            updated.
    """

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
    )

    created_at: datetime = Field(
        default=datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default=datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": datetime.now(timezone.utc)},
        nullable=False,
    )


class Product(BaseModel, table=True):
    """
    Represents a product available for purchase or customisation.

    Attributes:
        name (str): The name of the product.
        description (Optional[str]): The description of the product.
        category (str): The category of the product.
        base_price (float): The base price of the product.
        is_custom (bool): Whether the product is a custom product.
        parts (List[ProductPart]): The parts associated with the product.
    """

    __tablename__: str = "products"

    name: str
    category: str
    base_price: float
    is_custom: bool
    description: Optional[str] = None

    parts: List["ProductPart"] = Relationship(
        back_populates="product",
    )


class ProductPart(BaseModel, table=True):
    """
    Represents a part of a product (For a bike: Frame, Wheels, etc.).

    Attributes:
        product_id (UUID): The ID of the associated product.
        name (str): The name of the product part.
        product (Optional[Product]): The product that the part belongs to.
        variants (List[PartVariant]): The variants available for this
            product part.
    """

    __tablename__: str = "product_parts"

    name: str
    product_id: UUID = Field(foreign_key="products.id")

    product: Optional[Product] = Relationship(
        back_populates="parts",
    )
    variants: List["PartVariant"] = Relationship(
        back_populates="part",
    )


class PartVariant(BaseModel, table=True):
    """
    Represents a variant of a product part.

    Attributes:
        part_id (UUID): The ID of the associated product part.
        name (str): The name of the part variant.
        price (float): The price of the part variant.
        part (Optional[ProductPart]): The product part that this variant
            belongs to.
    """

    __tablename__: str = "part_variants"

    name: str
    price: float
    part_id: UUID = Field(foreign_key="product_parts.id")

    part: Optional[ProductPart] = Relationship(
        back_populates="variants",
    )
