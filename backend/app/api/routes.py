# app/api/routes.py

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status, Depends
from sqlmodel import Session

from app.database import get_session
from app.api.models import (
    Cart,
    CustomPrice,
    Product,
    ProductPart,
    PartVariant,
    VariantDependency,
)
from app.api.services import (
    create_cart_with_items,
    create_custom_price,
    create_product,
    create_variant_dependency,
    delete_custom_price,
    delete_variant_dependency,
    get_all_custom_prices,
    get_all_variant_dependencies,
    get_custom_price_by_id,
    get_product_by_id,
    get_all_products,
    get_variant_dependency_by_id,
    update_custom_price,
    update_product,
    delete_product,
    create_product_part,
    get_product_part_by_id,
    get_all_product_parts,
    update_product_part,
    delete_product_part,
    create_part_variant,
    get_part_variant_by_id,
    get_all_part_variants,
    update_part_variant,
    delete_part_variant,
    update_variant_dependency,
)
from app.api.schemas import (
    CartCreateSchema,
    CartSchema,
    CustomPriceCreateSchema,
    CustomPriceSchema,
    CustomPriceUpdateSchema,
    PartVariantCreateSchema,
    PartVariantSchema,
    PartVariantUpdateSchema,
    ProductCreateSchema,
    ProductPartCreateSchema,
    ProductPartSchema,
    ProductPartUpdateSchema,
    ProductSchema,
    ProductUpdateSchema,
    VariantDependencyCreateSchema,
    VariantDependencySchema,
    VariantDependencyUpdateSchema,
)
from app.api.utils import calculate_total_price

router = APIRouter()


@router.get("/healthchecker")
def healthcheck_route() -> dict:
    """
    Health check endpoint to verify that the API is live and running.

    Returns:
        dict: A dictionary containing a message indicating the API status.
    """
    return {"message": "API is Live"}


# Product Routes


@router.post("/products", response_model=ProductSchema)
def create_product_route(
    product: ProductCreateSchema,
    session: Session = Depends(get_session),
) -> Product:
    """
    This route allows for creating a new product. The `product` parameter
    contains all necessary details for the new product. The product is saved
    to the database and the created product is returned, serialised by the
    Pydantic schema.

    Args:
        product (Product): The product details to be created.
        session (Session): The database session for executing the queries.

    Returns:
        Product: The created product with its generated ID.
    """
    return create_product(session=session, product=product)


@router.get("/products/{product_id}", response_model=ProductSchema)
def get_product_route(
    product_id: UUID,
    session: Session = Depends(get_session),
) -> Product:
    """
    This route retrieves a product based on the provided `product_id`.
    If no product is found, a 404 error is raised.

    Args:
        product_id (UUID): The ID of the product to retrieve.
        session (Session): The database session for executing queries.

    Returns:
        Product: The product details if found.

    Raises:
        HTTPException: If the product is not found, a 404 error is raised.
    """
    product: Optional[Product] = get_product_by_id(
        session=session,
        product_id=product_id,
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@router.get("/products", response_model=List[ProductSchema])
def get_all_products__route(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
) -> List[Product]:
    """
    This route retrieves all products from the database. The list of
    products is returned as a response (serialised by the schema).

    Args:
        session (Session): The database session for executing queries.
        page (int): The page number used for the offset.
        page_size (int): The number of rows to limit the query.

    Returns:
        List[Product]: A list of all products.
    """
    return get_all_products(session=session, page=page, page_size=page_size)


@router.put("/products/{product_id}", response_model=ProductSchema)
def update_product_route(
    product_id: UUID,
    product_data: ProductUpdateSchema,
    session: Session = Depends(get_session),
) -> Product:
    """
    This route allows for partially updating the details of an
    existing product. The product's attributes can be modified
    by passing the `product_data` dictionary.
    If the product is not found, a 404 error is raised.

    Args:
        product_id (UUID): The ID of the product to update.
        product_data (dict): A dictionary containing only the
            fields to be updated.
        session (Session): The database session for executing queries.

    Returns:
        Product: The updated product details.

    Raises:
        HTTPException: If the product is not found, a 404 error is raised.
    """
    updated_product: Optional[Product] = update_product(
        session=session,
        product_id=product_id,
        product_data=product_data,
    )

    if not updated_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return updated_product


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product_route(
    product_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    """
    This route deletes a product from the database by its `product_id`.
    If the product is not found, a 404 error is raised.

    Args:
        product_id (UUID): The ID of the product to delete.
        session (Session): The database session for executing queries.

    Returns:
        None: with status HTTP_204_NO_CONTENT

    Raises:
        HTTPException: If the product is not found, a 404 error is raised.
    """
    if not delete_product(
        session=session,
        product_id=product_id,
    ):
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )


# Product Part Routes


@router.post("/product-parts", response_model=ProductPartSchema)
def create_product_part_route(
    part: ProductPartCreateSchema,
    session: Session = Depends(get_session),
) -> ProductPart:
    """
    This route allows for creating a new part for a product. The `part`
    parameter contains all necessary details for the new part. The part is
    saved to the database and the created part is returned, validated by
    the schema.

    Parts are generic groups of a customisable product, i.e. Wheels, Frame,
    Not the specific option for the parts, they do not have prices and
    merely exist to group the variants or options.

    Args:
        part (ProductPart): The part details to be created.
        session (Session): The database session for executing operations.

    Returns:
        ProductPart: The newly created product part with its generated ID.
    """
    return create_product_part(session=session, part=part)


@router.get("/product-parts/{part_id}", response_model=ProductPartSchema)
def get_product_part_route(
    part_id: UUID,
    session: Session = Depends(get_session),
) -> ProductPart:
    """
    This route retrieves a product part based on the provided `part_id`.
    If no part is found, a 404 error is raised.

    Args:
        part_id (UUID): The ID of the product part to retrieve.
        session (Session): The database session for executing queries.

    Returns:
        ProductPart: The product part details if found.

    Raises:
        HTTPException: If the product part is not found, a 404 error is raised.
    """
    part: Optional[ProductPart] = get_product_part_by_id(
        session=session,
        part_id=part_id,
    )
    if not part:
        raise HTTPException(
            status_code=404,
            detail="Product part not found",
        )

    return part


@router.get("/product-parts", response_model=List[ProductPartSchema])
def get_all_product_parts_route(
    session: Session = Depends(get_session),
) -> List[ProductPart]:
    """
    This route retrieves all product parts from the database. The list of
    product parts is returned as a response, serialised by the schema.

    Args:
        session (Session): The database session for executing operations.

    Returns:
        List[ProductPart]: A list of all product parts.
    """
    return get_all_product_parts(session=session)


@router.put("/product-parts/{part_id}", response_model=ProductPartSchema)
def update_product_part_route(
    part_id: UUID,
    part_data: ProductPartUpdateSchema,
    session: Session = Depends(get_session),
) -> ProductPart:
    """
    This route allows for updating the details of an existing product part.
    The part's attributes can be modified by passing the `part_data`
    dictionary.
    If the part is not found, a 404 error is raised.

    Args:
        part_id (UUID): The ID of the product part to update.
        part_data (dict): A dictionary containing only the fields to be
            updated.
        session (Session): The database session for executing operations.

    Returns:
        ProductPart: The updated product part details.

    Raises:
        HTTPException: If the product part is not found, a 404 error is raised.
    """
    updated_part: Optional[ProductPart] = update_product_part(
        session=session,
        part_id=part_id,
        part_data=part_data,
    )
    if not updated_part:
        raise HTTPException(
            status_code=404,
            detail="Product part not found",
        )

    return updated_part


@router.delete(
    "/product-parts/{part_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product_part_route(
    part_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    """
    This route deletes a product part from the system by its `part_id`.
    If the part is not found, a 404 error is raised.

    Args:
        part_id (UUID): The ID of the product part to delete.
        session (Session): The database session for executing queries.

    Returns:
        None: with status HTTP_204_NO_CONTENT

    Raises:
        HTTPException: If the product part is not found, a 404 error is raised.
    """
    if not delete_product_part(session=session, part_id=part_id):
        raise HTTPException(
            status_code=404,
            detail="Product part not found",
        )


# Part Variant Routes


@router.post("/part-variants", response_model=PartVariantSchema)
def create_part_variant_route(
    variant: PartVariantCreateSchema,
    session: Session = Depends(get_session),
) -> PartVariant:
    """
    This route allows for creating a new part variant. The `variant` parameter
    contains all necessary details for the new variant. The part variant is
    saved to the database and the created variant is returned, serialised by
    the schema.

    If the part is "Finish", the variant is "Matte" or "Shiny" and it has a
    base price.

    Args:
        variant (PartVariant): The part variant details to be created.
        session (Session): The database session for executing queries.

    Returns:
        PartVariant: The newly created part variant with its generated ID.
    """
    return create_part_variant(session=session, variant=variant)


@router.get("/part-variants/{variant_id}", response_model=PartVariantSchema)
def get_part_variant_route(
    variant_id: UUID,
    session: Session = Depends(get_session),
) -> PartVariant:
    """
    This route retrieves a part variant based on the provided `variant_id`.
    If no part variant is found, a 404 error is raised.

    Args:
        variant_id (UUID): The ID of the part variant to retrieve.
        session (Session): The database session for executing queries.

    Returns:
        PartVariant: The part variant details if found.

    Raises:
        HTTPException: If the part variant is not found, a 404 error is raised.
    """
    variant: Optional[PartVariant] = get_part_variant_by_id(
        session=session,
        variant_id=variant_id,
    )
    if not variant:
        raise HTTPException(
            status_code=404,
            detail="Part variant not found",
        )

    return variant


@router.get("/part-variants", response_model=List[PartVariantSchema])
def get_all_part_variants_route(
    session: Session = Depends(get_session),
) -> List[PartVariant]:
    """
    This route retrieves all part variants from the database. The list of
    part variants is returned as a response.

    Args:
        session (Session): The database session for executing operations.

    Returns:
        List[PartVariant]: A list of all part variants.
    """
    return get_all_part_variants(session=session)


@router.put("/part-variants/{variant_id}", response_model=PartVariantSchema)
def update_part_variant_route(
    variant_id: UUID,
    variant_data: PartVariantUpdateSchema,
    session: Session = Depends(get_session),
) -> PartVariant:
    """
    This route allows for partially updating the details of an
    existing part variant.
    The variant's attributes can be modified by passing the `variant_data`
    dictionary.
    If the part variant is not found, a 404 error is raised.

    Args:
        variant_id (UUID): The ID of the part variant to update.
        variant_data (dict): A dictionary containing the fields to be updated.
        session (Session): The database session for executing queries.

    Returns:
        PartVariant: The updated part variant details.

    Raises:
        HTTPException: If the part variant is not found, a 404 error is raised.
    """
    updated_variant: Optional[PartVariant] = update_part_variant(
        session=session,
        variant_id=variant_id,
        variant_data=variant_data,
    )
    if not updated_variant:
        raise HTTPException(
            status_code=404,
            detail="Part variant not found",
        )

    return updated_variant


@router.delete(
    "/part-variants/{variant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_part_variant_route(
    variant_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    """
    This route deletes a part variant from the system by its `variant_id`.
    If the part variant is not found, a 404 error is raised.

    Args:
        variant_id (UUID): The ID of the part variant to delete.
        session (Session): The database session for executing queries.

    Returns:
        None: with status HTTP_204_NO_CONTENT

    Raises:
        HTTPException: If the part variant is not found, a 404 error is raised.
    """
    if not delete_part_variant(session=session, variant_id=variant_id):
        raise HTTPException(
            status_code=404,
            detail="Part variant not found",
        )


# Variant Dependency Routes


@router.post("/variant-dependencies", response_model=VariantDependencySchema)
def create_variant_dependency_route(
    dependency: VariantDependencyCreateSchema,
    session: Session = Depends(get_session),
) -> VariantDependency:
    """
    This route allows for creating a new dependency for a part variant.
    The `dependency` parameter contains all necessary details for the
    new dependency. The dependency is saved to the database and the created
    dependency is returned.

    Args:
        dependency (VariantDependency): The variant dependency details
            to be created.
        session (Session): The database session for executing operations.

    Returns:
        VariantDependency: The newly created variant dependency with
            its generated ID.
    """
    return create_variant_dependency(session=session, dependency=dependency)


@router.get(
    "/variant-dependencies/{variant_id}",
    response_model=VariantDependencySchema,
)
def get_variant_dependency_route(
    variant_id: UUID,
    session: Session = Depends(get_session),
) -> VariantDependency:
    """
    This route retrieves a variant dependency based on the provided
    `variant_id`.
    If no variant dependency is found, a 404 error is raised.

    Args:
        variant_id (UUID): The ID of the variant dependency to retrieve.
        session (Session): The database session for executing operations.

    Returns:
        VariantDependency: The variant dependency details if found.

    Raises:
        HTTPException: If the variant dependency is not found, a 404
            error is raised.
    """
    dependency: Optional[VariantDependency] = get_variant_dependency_by_id(
        session=session,
        variant_id=variant_id,
    )
    if not dependency:
        raise HTTPException(
            status_code=404,
            detail="Variant dependency not found",
        )

    return dependency


@router.get(
    "/variant-dependencies",
    response_model=List[VariantDependencySchema],
)
def get_all_variant_dependencies_route(
    session: Session = Depends(get_session),
) -> List[VariantDependency]:
    """
    This route retrieves all variant dependencies from the database.
    The list of variant dependencies is returned as a response.

    Args:
        session (Session): The database session for executing operations.

    Returns:
        List[VariantDependency]: A list of all variant dependencies.
    """
    return get_all_variant_dependencies(session=session)


@router.put(
    "/variant-dependencies/{variant_id}",
    response_model=VariantDependencySchema,
)
def update_variant_dependency_route(
    variant_id: UUID,
    dependency_data: VariantDependencyUpdateSchema,
    session: Session = Depends(get_session),
) -> VariantDependency:
    """
    This route allows for updating the details of an existing variant
    dependency. It allows partial updates.
    The dependency's attributes can be modified by passing the
    `dependency_data` dictionary.
    If the variant dependency is not found, a 404 error is raised.

    Args:
        variant_id (UUID): The ID of the variant dependency to update.
        dependency_data (dict): A dictionary containing the fields to
            be updated.
        session (Session): The database session for executing operations.

    Returns:
        VariantDependency: The updated variant dependency details.

    Raises:
        HTTPException: If the variant dependency is not found, a 404
            error is raised.
    """
    updated_dependency: Optional[VariantDependency] = (
        update_variant_dependency(  # noqa: E501
            session=session,
            variant_id=variant_id,
            dependency_data=dependency_data,
        )
    )
    if not updated_dependency:
        raise HTTPException(
            status_code=404,
            detail="Variant dependency not found",
        )

    return updated_dependency


@router.delete(
    "/variant-dependencies/{variant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_variant_dependency_route(
    variant_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    """
    This route deletes a variant dependency from the system by its
    `variant_id`.
    If the variant dependency is not found, a 404 error is raised.

    Args:
        variant_id (UUID): The ID of the variant dependency to delete.
        session (Session): The database session for executing operations.

    Returns:
        None: with status HTTP_204_NO_CONTENT

    Raises:
        HTTPException: If the variant dependency is not found, a 404
            error is raised.
    """
    if not delete_variant_dependency(session=session, variant_id=variant_id):
        raise HTTPException(
            status_code=404,
            detail="Variant dependency not found",
        )


# Custom Price Routes


@router.post("/custom-prices", response_model=CustomPriceSchema)
def create_custom_price_route(
    custom_price: CustomPriceCreateSchema,
    session: Session = Depends(get_session),
) -> CustomPrice:
    """
    This route allows for creating a new custom price. The
    `custom_price` parameter contains all necessary details for
    the new custom price. The custom price is saved to the database
    and the created custom price is returned.

    Args:
        custom_price (CustomPrice): The custom price details to be created.
        session (Session): The database session for executing operations.

    Returns:
        CustomPrice: The newly created custom price with its generated ID.
    """
    return create_custom_price(session=session, custom_price=custom_price)


@router.get(
    "/custom-prices/{custom_price_id}",
    response_model=CustomPriceSchema,
)
def get_custom_price_route(
    custom_price_id: UUID,
    session: Session = Depends(get_session),
) -> CustomPrice:
    """
    This route retrieves a custom price based on the provided
    `custom_price_id`.
    If no custom price is found, a 404 error is raised.

    Args:
        custom_price_id (UUID): The ID of the custom price to retrieve.
        session (Session): The database session for executing operations.

    Returns:
        CustomPrice: The custom price details if found.

    Raises:
        HTTPException: If the custom price is not found, a 404 error
            is raised.
    """
    custom_price: Optional[CustomPrice] = get_custom_price_by_id(
        session=session,
        custom_price_id=custom_price_id,
    )
    if not custom_price:
        raise HTTPException(
            status_code=404,
            detail="Custom price not found",
        )

    return custom_price


@router.get("/custom-prices", response_model=List[CustomPriceSchema])
def get_all_custom_prices_route(
    session: Session = Depends(get_session),
) -> List[CustomPrice]:
    """
    This route retrieves all custom prices from the database. The list of
    custom prices is returned as a response.

    Args:
        session (Session): The database session for executing operations.

    Returns:
        List[CustomPrice]: A list of all custom prices.
    """
    return get_all_custom_prices(session=session)


@router.put(
    "/custom-prices/{custom_price_id}",
    response_model=CustomPriceSchema,
)
def update_custom_price_route(
    custom_price_id: UUID,
    custom_price_data: CustomPriceUpdateSchema,
    session: Session = Depends(get_session),
) -> CustomPrice:
    """
    This route allows for updating the details of an existing
    custom price.
    The custom price's attributes can be modified by passing
    the `custom_price_data` dictionary.
    If the custom price is not found, a 404 error is raised.

    Args:
        custom_price_id (UUID): The ID of the custom price to update.
        custom_price_data (dict): A dictionary containing the fields
            to be updated.
        session (Session): The database session for executing operations.

    Returns:
        CustomPrice: The updated custom price details.

    Raises:
        HTTPException: If the custom price is not found, a 404 error is raised.
    """
    updated_price: Optional[CustomPrice] = update_custom_price(
        session=session,
        custom_price_id=custom_price_id,
        custom_price_data=custom_price_data,
    )
    if not updated_price:
        raise HTTPException(
            status_code=404,
            detail="Custom price not found",
        )

    return updated_price


@router.delete(
    "/custom-prices/{custom_price_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_custom_price_route(
    custom_price_id: UUID,
    session: Session = Depends(get_session),
) -> None:
    """
    This route deletes a custom price from the system by its `custom_price_id`.
    If the custom price is not found, a 404 error is raised.

    Args:
        custom_price_id (UUID): The ID of the custom price to delete.
        session (Session): The database session for executing operations.

    Returns:
        None: with status HTTP_204_NO_CONTENT

    Raises:
        HTTPException: If the custom price is not found, a 404 error is raised.
    """
    if not delete_custom_price(
        session=session,
        custom_price_id=custom_price_id,
    ):
        raise HTTPException(
            status_code=404,
            detail="Custom price not found",
        )


# Carts routes


@router.post("/carts", response_model=CartSchema)
def create_cart_with_items_route(
    cart_data: CartCreateSchema,
    session: Session = Depends(get_session),
) -> Cart:
    """
    Create a new cart and add a list of items to it in bulk.

    This route creates a new cart for a user, and adds multiple items to the
    cart based on the `items` parameter. The `items` are provided as a list of
    CartItem objects. After the cart is created and the items are added, the
    created cart is returned.

    Args:
        cart_data (CartCreateSchema): An object for a Cart and a list of
            CartItem objects to be added to the cart.
        session (Session): The database session for executing operations.

    Returns:
        Cart: The newly created cart with the added items.

    Raises:
        HTTPException: If an error occurs during cart creation or item
        addition, a 400 error with the exception message is raised.
    """
    try:
        cart: Cart = create_cart_with_items(
            session=session,
            cart_data=cart_data,
        )

        return cart

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Pricing routes


@router.post("/calculate-price", response_model=float)
def calculate_total_price_route(
    product_id: UUID,
    variant_ids: List[UUID],
    session: Session = Depends(get_session),
) -> dict:
    """
    Calculate the total price of a product with selected variants.

    This route calculates the total price for a product based on its ID and
    the list of variant IDs provided. The `product_id` refers to the base
    product, and the `variant_ids` are additional variants added to the
    product. The calculated total price is returned.

    Args:
        product_id (UUID): The ID of the base product.
        variant_ids (List[UUID]): A list of variant IDs selected for
            the product.
        session (Session): The database session for executing operations.

    Returns:
        dict: A dictionary containing the total price of the product as
            a float.
    """
    total_price: float = calculate_total_price(
        session=session,
        product_id=product_id,
        selected_variant_ids=variant_ids,
    )

    return {"message": total_price}
