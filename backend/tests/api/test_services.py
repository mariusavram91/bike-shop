# tests/api/test_services.py

from uuid import UUID, uuid4
from typing import Any, List, Optional

import pytest
from sqlmodel import Session

from app.api.models import (
    Product,
    ProductPart,
    PartVariant,
)
from app.api.services import (
    create_product,
    get_product_by_id,
    get_all_products,
    update_product,
    delete_product,
    create_product_part,
)
from app.api.schemas import (
    ProductCreateSchema,
    ProductPartCreateSchema,
    ProductUpdateSchema,
)


@pytest.fixture
def sample_data(test_db: Session) -> dict[str, Any]:
    product = Product(
        id=uuid4(),
        name="Test Product",
        description="A sample product",
        category="Bicycle",
        base_price=100.0,
        is_custom=False,
        is_available=True,
        stock_quantity=10,
    )
    another_product = Product(
        id=uuid4(),
        name="Another Test Product",
        description="Another sample product",
        category="Surfboard",
        base_price=500.0,
        is_custom=False,
        is_available=True,
        stock_quantity=5,
    )
    test_db.add_all([product, another_product])

    product_part1 = ProductPart(
        id=uuid4(),
        product_id=product.id,
        name="Test Product Part 1",
    )
    product_part2 = ProductPart(
        id=uuid4(),
        product_id=product.id,
        name="Test Product Part 2",
    )
    test_db.add_all([product_part1, product_part2])

    variant1 = PartVariant(
        id=uuid4(),
        part_id=uuid4(),
        name="Variant 1",
        price=20.0,
        is_available=True,
        stock_quantity=5,
    )
    variant2 = PartVariant(
        id=uuid4(),
        part_id=uuid4(),
        name="Variant 2",
        price=30.0,
        is_available=True,
        stock_quantity=3,
    )
    variant3 = PartVariant(
        id=uuid4(),
        part_id=uuid4(),
        name="Variant 3 (Out of Stock)",
        price=15.0,
        is_available=True,
        stock_quantity=0,
    )
    test_db.add_all([variant1, variant2, variant3])

    test_db.commit()

    return {
        "product": product,
        "another_product": another_product,
        "variants": [variant1, variant2, variant3],
        "parts": [product_part1, product_part2],
    }


# Product tests


def test_create_product_success(test_db: Session) -> None:
    product = ProductCreateSchema(
        name="Test Product",
        description="A sample product",
        category="Electronics",
        base_price=100.0,
        is_custom=False,
        is_available=True,
        stock_quantity=10,
    )
    created_product: Product = create_product(test_db, product)

    assert created_product.id is not None
    assert created_product.name == "Test Product"
    assert created_product.base_price == 100.0


def test_get_product_by_id_success(
    test_db: Session,
    sample_data: dict[str, Any],
) -> None:
    product: Product = sample_data["product"]

    fetched_product: Optional[Product] = get_product_by_id(test_db, product.id)

    assert fetched_product is not None
    assert fetched_product.id == product.id
    assert fetched_product.name == "Test Product"


def test_get_product_by_id_not_found(test_db: Session) -> None:
    invalid_id: UUID = uuid4()
    fetched_product: Optional[Product] = get_product_by_id(
        test_db,
        invalid_id,
    )

    assert fetched_product is None


def test_get_all_products_success(
    test_db: Session,
    sample_data: dict[str, Any],
) -> None:
    products: List[Product] = get_all_products(test_db)

    assert len(products) == 2
    assert products[0].name == sample_data["product"].name
    assert products[1].name == sample_data["another_product"].name


def test_get_all_products_empty(test_db: Session) -> None:
    products: List[Product] = get_all_products(test_db)

    assert len(products) == 0


def test_update_product_success(
    test_db: Session,
    sample_data: dict[str, Any],
) -> None:
    product: Product = sample_data["product"]

    updated_product: Optional[Product] = update_product(
        test_db,
        product.id,
        ProductUpdateSchema(
            name="New Name",
            base_price=120.0,
        ),
    )

    assert updated_product is not None
    assert updated_product.name == "New Name"
    assert updated_product.base_price == 120.0


def test_update_product_not_found(test_db: Session) -> None:
    invalid_id: UUID = uuid4()
    updated_product: Optional[Product] = update_product(
        test_db,
        invalid_id,
        ProductUpdateSchema(name="Non-existent Product"),
    )
    assert updated_product is None


def test_delete_product_success(
    test_db: Session,
    sample_data: dict[str, Any],
) -> None:
    product: Product = sample_data["another_product"]

    result: bool = delete_product(test_db, product.id)
    assert result is True

    fetched_product: Optional[Product] = get_product_by_id(test_db, product.id)
    assert fetched_product is None


def test_delete_product_not_found(test_db: Session) -> None:
    invalid_id: UUID = uuid4()
    result: bool = delete_product(test_db, invalid_id)

    assert result is False


# Parts test


def test_create_product_part_success(test_db: Session) -> None:
    part = ProductPartCreateSchema(
        product_id=uuid4(),
        name="Test Product Part",
    )
    created_part: ProductPart = create_product_part(test_db, part)

    assert created_part.name == "Test Product Part"
