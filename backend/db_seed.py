# db_seed.py

from sqlmodel import Session

from app.database import engine

from app.api.models import (
    CustomPrice,
    Product,
    ProductPart,
    PartVariant,
    VariantDependency,
)


def seed_data(session: Session) -> None:
    mountain_bike = Product(
        name="Mountain Bike",
        description="Built for rugged trails and tough terrain.",
        category="Bike",
        base_price=800.00,
        is_custom=False,  # Not customisable
        is_available=True,
        stock_quantity=5,
    )

    road_bike = Product(
        name="Road Bike",
        description="A high-performance road bike for fast rides.",
        category="Bike",
        base_price=200.00,
        is_custom=True,  # This is customisable
        is_available=True,
        stock_quantity=10,
    )

    mountain_bike_2 = Product(
        name="Mountain Bike",
        description="Built for rugged trails and tough terrain.",
        category="Bike",
        base_price=800.00,
        is_custom=False,  # Not customisable
        is_available=True,
        stock_quantity=5,
    )

    fixed_gear_bike = Product(
        name="Fixed-Gear Bike",
        category="Bike",
        base_price=920.00,
        is_custom=False,  # Not customisable
        is_available=False,  # Not in stock
        stock_quantity=0,
    )

    session.add(road_bike)
    session.add(mountain_bike)
    session.add(mountain_bike_2)
    session.add(fixed_gear_bike)

    road_bike_handlebar = ProductPart(
        product_id=road_bike.id,
        name="Handlebar",
    )

    road_bike_frame = ProductPart(
        product_id=road_bike.id,
        name="Frame",
    )

    road_bike_wheel = ProductPart(
        product_id=road_bike.id,
        name="Wheels",
    )

    road_bike_finish = ProductPart(
        product_id=road_bike.id,
        name="Finish",
    )

    session.add(road_bike_handlebar)
    session.add(road_bike_wheel)
    session.add(road_bike_frame)
    session.add(road_bike_finish)

    # Create Part Variants (for customisable products)
    road_bike_handlebar_variant = PartVariant(
        part_id=road_bike_handlebar.id,
        name="Standard Road Handlebar",
        price=100.00,
        is_available=True,
        stock_quantity=15,
    )

    road_bike_handlebar_variant_2 = PartVariant(
        part_id=road_bike_handlebar.id,
        name="Custom Carbon Fiber Road Handlebar",
        price=200.00,
        is_available=True,
        stock_quantity=5,
    )

    road_bike_wheel_variant = PartVariant(
        part_id=road_bike_wheel.id,
        name="Standard Road Wheel",
        price=200.00,
        is_available=True,
        stock_quantity=10,
    )

    road_bike_wheel_variant_2 = PartVariant(
        part_id=road_bike_wheel.id,
        name="Thin Road Wheel",
        price=240.00,
        is_available=True,
        stock_quantity=5,
    )

    road_bike_frame_variant = PartVariant(
        part_id=road_bike_frame.id,
        name="Standard Road Frame",
        price=100.00,
        is_available=True,
        stock_quantity=10,
    )

    road_bike_frame_variant_2 = PartVariant(
        part_id=road_bike_frame.id,
        name="Diamond Road Frame",
        price=200.00,
        is_available=True,
        stock_quantity=10,
    )

    road_bike_finish_variant = PartVariant(
        part_id=road_bike_finish.id,
        name="Matte",
        price=100.00,
        is_available=True,
        stock_quantity=15,
    )

    road_bike_finish_variant_2 = PartVariant(
        part_id=road_bike_finish.id,
        name="Shiny",
        price=200.00,
        is_available=True,
        stock_quantity=5,
    )

    session.add(road_bike_handlebar_variant)
    session.add(road_bike_handlebar_variant_2)
    session.add(road_bike_wheel_variant)
    session.add(road_bike_wheel_variant_2)
    session.add(road_bike_frame_variant)
    session.add(road_bike_frame_variant_2)
    session.add(road_bike_finish_variant)
    session.add(road_bike_finish_variant_2)

    # Add Custom Prices for custom parts
    finish_custom_price = CustomPrice(
        variant_id=road_bike_finish_variant.id,
        dependent_variant_id=road_bike_frame_variant_2.id,
        custom_price=50.00,
    )

    handlebar_custom_price = CustomPrice(
        variant_id=road_bike_handlebar_variant_2.id,
        dependent_variant_id=road_bike_frame_variant_2.id,
        custom_price=90.00,
    )

    session.add(finish_custom_price)
    session.add(handlebar_custom_price)

    # Create Variant Dependencies
    wheels_dependency_frame = VariantDependency(
        variant_id=road_bike_wheel_variant_2.id,
        restrictions=f"{road_bike_frame_variant.id}",
    )

    frame_dependency_finish = VariantDependency(
        variant_id=road_bike_frame_variant_2.id,
        restrictions=f"{road_bike_finish_variant.id}",
    )

    session.add(wheels_dependency_frame)
    session.add(frame_dependency_finish)

    session.commit()


def seed() -> None:
    """
    Seed the database with realistic data for a customisable bike shop.

    This function will add products (both customisable and non-customisable),
    product parts, part variants to the db.

    Returns:
        None
    """
    with Session(engine) as session:
        seed_data(session)


if __name__ == "__main__":
    seed()
    print("Database seeded successfully.")
