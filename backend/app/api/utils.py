# app/api/utils.py

from uuid import UUID
from typing import List, Optional, Sequence

from sqlmodel import Session, select

from app.api.models import CustomPrice, Product, PartVariant


def calculate_total_price(
    session: Session,
    product_id: UUID,
    selected_variant_ids: List[UUID],
) -> float:
    """
    Calculate the total price of selected part variants.

    It searches for all custom prices of each variant and adjusts
    the total price based on that. The custom price is just an
    addition to the variant's base price.

    Args:
        variant_ids: A list of UUIDs of the selected part variants.
        session: Database session dependency.

    Returns:
        Total price of the selected part variants.

    Raises:
        HTTPException: If any of the part variants are not available or out
        of stock.
    """
    product: Optional[Product] = session.get(Product, product_id)
    if not product:
        raise ValueError(f"Product with ID {product_id} not found.")

    total_price: float = product.base_price

    for variant_id in selected_variant_ids:
        variant: Optional[PartVariant] = session.get(PartVariant, variant_id)
        if not variant:
            raise ValueError(f"Variant with ID {variant_id} not found.")
        if not variant.is_available or variant.stock_quantity <= 0:
            raise ValueError(f"Variant with ID {variant_id} is out of stock.")

        total_price += variant.price

        custom_prices: Sequence[CustomPrice] = session.exec(
            select(CustomPrice).where(
                CustomPrice.variant_id == variant_id,
            )
        ).all()

        for custom_price_entry in custom_prices:
            if custom_price_entry.dependent_variant_id in selected_variant_ids:
                total_price += custom_price_entry.custom_price

    return total_price
