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
        is_available (bool): Whether the product is available for purchase.
        stock_quantity (int): The quantity of the product in stock.
        parts (List[ProductPart]): The parts associated with the product.
        cart_items (List[CartItem]): The cart items that contain this product.
    """

    __tablename__: str = "products"

    name: str
    category: str
    base_price: float
    is_custom: bool
    description: Optional[str] = None
    is_available: bool
    stock_quantity: int

    parts: List["ProductPart"] = Relationship(
        back_populates="product",
    )
    cart_items: List["CartItem"] = Relationship(
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
        is_available (bool): Whether the part variant is available for
            selection.
        stock_quantity (int): The stock quantity of the part variant.
        part (Optional[ProductPart]): The product part that this variant
            belongs to.
    """

    __tablename__: str = "part_variants"

    name: str
    price: float
    is_available: bool
    stock_quantity: int
    part_id: UUID = Field(foreign_key="product_parts.id")

    part: Optional[ProductPart] = Relationship(
        back_populates="variants",
    )
    dependencies: List["VariantDependency"] = Relationship(
        back_populates="variant",
    )


class VariantDependency(SQLModel, table=True):
    """
    Represents a dependency between two part variants. Any ids in the
    restrictions field should make variant unavailable.

    Attributes:
        variant_id (UUID): The ID of the variant this dependency is
            related to.
        restrictions (Optional[str]): Any restrictions related to
            the dependency.
        variant (Optional[PartVariant]): The part variant that this
            dependency applies to.
    """

    __tablename__: str = "variant_dependencies"

    variant_id: UUID = Field(
        foreign_key="part_variants.id",
        primary_key=True,
    )
    restrictions: Optional[str]

    variant: Optional[PartVariant] = Relationship(
        back_populates="dependencies",
    )


class Cart(BaseModel, table=True):
    """
    Represents a shopping cart. It omits the user for the moment.

    Attributes:
        purchased (bool): Whether the cart has been purchased or not.
        total_price (float): The total price of the cart including all
            products.
        items (List[CartItem]): The items contained in the cart.
    """

    __tablename__: str = "carts"

    purchased: bool
    total_price: float

    items: List["CartItem"] = Relationship(
        back_populates="cart",
    )


class CartItem(BaseModel, table=True):
    """
    Represents an item in a shopping cart.

    Attributes:
        cart_id (UUID): The ID of the cart that the item belongs to.
        product_id (UUID): The ID of the product for this item.
        selected_parts (Optional[str]): A string containing selected parts
            ids for the item, separated by commas.
        total_price (float): The total price of the item.
        cart (Optional[Cart]): The cart that this item belongs to.
        product (Optional[Product]): The product associated with the cart item.
    """

    __tablename__: str = "cart_items"

    cart_id: UUID = Field(foreign_key="carts.id")
    product_id: UUID = Field(foreign_key="products.id")
    selected_parts: Optional[str]
    total_price: float

    cart: Optional[Cart] = Relationship(
        back_populates="items",
    )
    product: Optional[Product] = Relationship(
        back_populates="cart_items",
    )
