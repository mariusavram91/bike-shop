# app/api/services.py

from uuid import UUID
from typing import Optional, List, Sequence

from sqlmodel import select
from sqlmodel.sql._expression_select_cls import SelectOfScalar

from app.database import Session
from app.api.models import (
    Cart,
    CartItem,
    Product,
    ProductPart,
    PartVariant,
    VariantDependency,
)
from app.api.schemas import (
    CartCreateSchema,
    PartVariantCreateSchema,
    PartVariantUpdateSchema,
    ProductCreateSchema,
    ProductPartCreateSchema,
    ProductPartUpdateSchema,
    ProductUpdateSchema,
    VariantDependencyCreateSchema,
    VariantDependencyUpdateSchema,
)

# Products CRUD


def create_product(
    session: Session,
    product: ProductCreateSchema,
) -> Product:
    """
    Create a new product in the database.

    Args:
        session (Session): The database session.
        product (Product): The product object to be added.

    Returns:
        Product: The newly created product with a populated `id` field.
    """
    created_product = Product(**product.model_dump())

    session.add(created_product)
    session.commit()
    session.refresh(created_product)

    return created_product


def get_product_by_id(
    session: Session,
    product_id: UUID,
) -> Optional[Product]:
    """
    Retrieve a product from the database by its ID.

    Args:
        session (Session): The database session.
        product_id (UUID): The ID of the product to retrieve.

    Returns:
        Optional[Product]: The product object if found, otherwise None.
    """
    return session.get(Product, product_id)


def get_all_products(
    session: Session,
    page: int = 1,
    page_size: int = 10,
) -> List[Product]:
    """
    Retrieve all products from the database.

    Args:
        session (Session): The database session.
        page (int): The page number used for the offset.
        page_size (int): The number of rows to limit the query.

    Returns:
        List[Product]: A list of all products in the database.
    """
    offset: int = (page - 1) * page_size

    statement: SelectOfScalar[Product] = (
        select(Product)
        .limit(
            page_size,
        )
        .offset(
            offset,
        )
    )
    products: Sequence[Product] = session.exec(statement).all()

    return list(products)


def update_product(
    session: Session,
    product_id: UUID,
    product_data: ProductUpdateSchema,
) -> Optional[Product]:
    """
    Update an existing product in the database.

    Args:
        session (Session): The database session.
        product_id (UUID): The ID of the product to update.
        product_data (dict): The product attributes to update.

    Returns:
        Optional[Product]: The updated product if found, otherwise None.
    """
    product: Optional[Product] = session.get(Product, product_id)
    if not product:
        return None

    for key, value in product_data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    session.commit()
    session.refresh(product)

    return product


def delete_product(
    session: Session,
    product_id: UUID,
) -> bool:
    """
    Delete a product from the database by its ID.

    Args:
        session (Session): The database session.
        product_id (UUID): The ID of the product to delete.

    Returns:
        bool: True if the product was deleted, False if not found.
    """
    product: Optional[Product] = session.get(Product, product_id)
    if not product:
        return False

    session.delete(product)
    session.commit()

    return True


# Product Parts CRUD


def create_product_part(
    session: Session,
    part: ProductPartCreateSchema,
) -> ProductPart:
    """
    Create a new product part in the database.

    Args:
        session (Session): The database session.
        part (ProductPart): The product part object to be added.

    Returns:
        ProductPart: The newly created product part with a populated `id`
            field.
    """
    created_part = ProductPart(**part.model_dump())

    session.add(created_part)
    session.commit()
    session.refresh(created_part)

    return created_part


def update_product_part(
    session: Session,
    part_id: UUID,
    part_data: ProductPartUpdateSchema,
) -> Optional[ProductPart]:
    """
    Update an existing product part in the database.

    Args:
        session (Session): The database session.
        part_id (UUID): The ID of the product part to update.
        part_data (dict): The product part attributes to update.

    Returns:
        Optional[ProductPart]: The updated product part if found, otherwise
            None.
    """
    part: Optional[ProductPart] = session.get(ProductPart, part_id)
    if not part:
        return None

    for key, value in part_data.model_dump(exclude_unset=True).items():
        setattr(part, key, value)

    session.commit()
    session.refresh(part)

    return part


def get_product_part_by_id(
    session: Session,
    part_id: UUID,
) -> Optional[ProductPart]:
    """
    Retrieve a product part from the database by its ID.

    Args:
        session (Session): The database session.
        part_id (UUID): The ID of the product part to retrieve.

    Returns:
        Optional[ProductPart]: The product part object if found, otherwise
            None.
    """
    return session.get(ProductPart, part_id)


def get_all_product_parts(
    session: Session,
) -> List[ProductPart]:
    """
    Retrieve all product parts from the database.

    Args:
        session (Session): The database session.

    Returns:
        List[ProductPart]: A list of all product parts in the database.
    """
    statement: SelectOfScalar[ProductPart] = select(ProductPart)
    product_parts: Sequence[ProductPart] = session.exec(statement).all()

    return list(product_parts)


def delete_product_part(
    session: Session,
    part_id: UUID,
) -> bool:
    """
    Delete a product part from the database by its ID.

    Args:
        session (Session): The database session.
        part_id (UUID): The ID of the product part to delete.

    Returns:
        bool: True if the product part was deleted, False if not found.
    """
    part: Optional[ProductPart] = session.get(
        ProductPart,
        part_id,
    )
    if not part:
        return False

    session.delete(part)
    session.commit()

    return True


# Part Variants CRUD


def create_part_variant(
    session: Session,
    variant: PartVariantCreateSchema,
) -> PartVariant:
    """
    Create a new part variant in the database.

    Args:
        session (Session): The database session.
        variant (PartVariant): The part variant object to be added.

    Returns:
        PartVariant: The newly created part variant with a populated `id`
            field.
    """
    created_variant = PartVariant(**variant.model_dump())

    session.add(created_variant)
    session.commit()
    session.refresh(created_variant)

    return created_variant


def get_part_variant_by_id(
    session: Session,
    variant_id: UUID,
) -> Optional[PartVariant]:
    """
    Retrieve a part variant from the database by its ID.

    Args:
        session (Session): The database session.
        variant_id (UUID): The ID of the part variant to retrieve.

    Returns:
        Optional[PartVariant]: The part variant object if found,
            otherwise None.
    """
    return session.get(PartVariant, variant_id)


def get_all_part_variants(
    session: Session,
) -> List[PartVariant]:
    """
    Retrieve all part variants from the database.

    Args:
        session (Session): The database session.

    Returns:
        List[PartVariant]: A list of all part variants in the database.
    """
    statement: SelectOfScalar[PartVariant] = select(PartVariant)
    part_variants: Sequence[PartVariant] = session.exec(statement).all()

    return list(part_variants)


def update_part_variant(
    session: Session,
    variant_id: UUID,
    variant_data: PartVariantUpdateSchema,
) -> Optional[PartVariant]:
    """
    Update an existing part variant in the database.

    Args:
        session (Session): The database session.
        variant_id (UUID): The ID of the part variant to update.
        variant_data (dict): The part variant attributes to update.

    Returns:
        Optional[PartVariant]: The updated part variant if found,
            otherwise None.
    """
    variant: Optional[PartVariant] = session.get(
        PartVariant,
        variant_id,
    )
    if not variant:
        return None

    for key, value in variant_data.model_dump(exclude_unset=True).items():
        setattr(variant, key, value)

    session.commit()
    session.refresh(variant)

    return variant


def delete_part_variant(
    session: Session,
    variant_id: UUID,
) -> bool:
    """
    Delete a part variant from the database by its ID.

    Args:
        session (Session): The database session.
        variant_id (UUID): The ID of the part variant to delete.

    Returns:
        bool: True if the part variant was deleted, False if not
            found.
    """
    variant: Optional[PartVariant] = session.get(
        PartVariant,
        variant_id,
    )
    if not variant:
        return False

    session.delete(variant)
    session.commit()

    return True


# Variant Dependencies CRUD


def create_variant_dependency(
    session: Session,
    dependency: VariantDependencyCreateSchema,
) -> VariantDependency:
    """
    Create a new variant dependency in the database.

    Args:
        session (Session): The database session.
        dependency (VariantDependency): The variant dependency object
            to be added.

    Returns:
        VariantDependency: The newly created variant dependency
            with a populated `id` field.
    """
    created_dependency = VariantDependency(**dependency.model_dump())

    session.add(created_dependency)
    session.commit()
    session.refresh(created_dependency)

    return created_dependency


def get_variant_dependency_by_id(
    session: Session,
    variant_id: UUID,
) -> Optional[VariantDependency]:
    """
    Retrieve a variant dependency from the database by its ID.

    Args:
        session (Session): The database session.
        variant_id (UUID): The ID of the variant dependency to retrieve.

    Returns:
        Optional[VariantDependency]: The variant dependency object
            if found, otherwise None.
    """
    return session.get(VariantDependency, variant_id)


def get_all_variant_dependencies(
    session: Session,
) -> List[VariantDependency]:
    """
    Retrieve all variant dependencies from the database.

    Args:
        session (Session): The database session.

    Returns:
        List[VariantDependency]: A list of all variant dependencies
            in the database.
    """
    variant_dependencies: Sequence[VariantDependency] = session.exec(
        select(VariantDependency)
    ).all()

    return list(variant_dependencies)


def update_variant_dependency(
    session: Session,
    variant_id: UUID,
    dependency_data: VariantDependencyUpdateSchema,
) -> Optional[VariantDependency]:
    """
    Update an existing variant dependency in the database.

    Args:
        session (Session): The database session.
        variant_id (UUID): The ID of the variant dependency to update.
        dependency_data (dict): The variant dependency attributes to
            update.

    Returns:
        Optional[VariantDependency]: The updated variant dependency
            if found, otherwise None.
    """
    dependency: Optional[VariantDependency] = session.get(
        VariantDependency,
        variant_id,
    )
    if not dependency:
        return None

    for key, value in dependency_data.model_dump(exclude_unset=True).items():
        setattr(dependency, key, value)

    session.commit()
    session.refresh(dependency)

    return dependency


def delete_variant_dependency(
    session: Session,
    variant_id: UUID,
) -> bool:
    """
    Delete a variant dependency from the database by its ID.

    Args:
        session (Session): The database session.
        variant_id (UUID): The ID of the variant dependency to delete.

    Returns:
        bool: True if the variant dependency was deleted, False if
            not found.
    """
    dependency: Optional[VariantDependency] = session.get(
        VariantDependency,
        variant_id,
    )
    if not dependency:
        return False

    session.delete(dependency)
    session.commit()

    return True


# Cart CRUD


def create_cart_with_items(
    session: Session,
    cart_data: CartCreateSchema,
) -> Cart:
    """
    Create a new cart and add multiple items to it in a single transaction.

    Args:
        session (Session): The database session.
        cart_data (CartCreateSchema): A cart object with a list of
            cart items, where each dictionary contains product ID,
            selected parts, and total price.

    Returns:
        Cart: The newly created cart with its associated items.
    """
    cart = Cart(
        purchased=False,
        total_price=cart_data.total_price,
    )
    session.add(cart)

    cart_items: List[CartItem] = [
        CartItem(
            cart_id=cart.id,
            product_id=item.product_id,
            selected_parts=item.selected_parts,
            total_price=item.total_price,
        )
        for item in cart_data.items
    ]

    session.add_all(cart_items)

    session.commit()
    session.refresh(cart)

    return cart
