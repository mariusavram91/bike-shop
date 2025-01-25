# tests/api/test_utils.py

from typing import Any, List
from uuid import uuid4

import pytest
from sqlmodel import Session

from app.api.models import Product, PartVariant
from app.api.utils import calculate_total_price


@pytest.fixture
def sample_data(test_db: Session) -> dict[str, Any]:
    product = Product(
        id=uuid4(),
        name="Test Product",
        description="A sample product",
        category="Electronics",
        base_price=100.0,
        is_custom=False,
        is_available=True,
        stock_quantity=10,
    )
    test_db.add(product)

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
        "variants": [variant1, variant2, variant3],
    }


def test_calculate_total_price_valid(
    test_db: Session,
    sample_data: dict[str, Any],
) -> None:
    product: Product = sample_data["product"]
    variants: List[PartVariant] = sample_data["variants"]

    total_price: float = calculate_total_price(
        test_db,
        product_id=product.id,
        selected_variant_ids=[variants[0].id, variants[1].id],
    )
    assert total_price == (
        product.base_price  # 100
        + variants[0].price  # + 20
        + variants[1].price  # + 30
    )


def test_calculate_total_price_variant_out_of_stock(
    test_db: Session, sample_data: dict[str, Any]
) -> None:
    product: Product = sample_data["product"]
    variants: List[PartVariant] = sample_data["variants"]

    with pytest.raises(ValueError, match="is out of stock"):
        calculate_total_price(
            test_db,
            product_id=product.id,
            selected_variant_ids=[variants[2].id],  # Out of stock variant
        )


def test_calculate_total_price_product_not_found(
    test_db: Session,
) -> None:
    with pytest.raises(ValueError, match="Product with ID .* not found"):
        calculate_total_price(
            test_db,
            product_id=uuid4(),
            selected_variant_ids=[],
        )


def test_calculate_total_price_variant_not_found(
    test_db: Session,
    sample_data: dict[str, Any],
) -> None:
    product: Product = sample_data["product"]

    with pytest.raises(ValueError, match="Variant with ID .* not found"):
        calculate_total_price(
            test_db,
            product_id=product.id,
            selected_variant_ids=[uuid4()],  # Non-existent variant ID
        )


def test_calculate_total_price_no_variants_selected(
    test_db: Session,
    sample_data: dict[str, Any],
) -> None:
    product: Product = sample_data["product"]

    total_price: float = calculate_total_price(
        test_db,
        product_id=product.id,
        selected_variant_ids=[],
    )
    assert total_price == product.base_price
