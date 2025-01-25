# app/api/utils.py

from uuid import UUID
from typing import List, Optional

from sqlmodel import Session

from app.api.models import Product, PartVariant


def calculate_total_price(
    session: Session,
    product_id: UUID,
    selected_variant_ids: List[UUID],
) -> float:
    """
    Calculate the total price of selected part variants.

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

    return total_price
