# tests/api/test_routes.py

from uuid import uuid4

from fastapi.testclient import TestClient
from httpx import Response
from sqlmodel import Session

from app.api.models import Product
from app.api.services import create_product
from app.api.schemas import ProductCreateSchema


def test_healthcheck(test_client: TestClient) -> None:
    response: Response = test_client.get("/api/v1/healthchecker")

    assert response.status_code == 200
    assert response.json() == {"message": "API is Live"}


def test_create_product(test_client: TestClient) -> None:
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "base_price": 100.0,
        "category": "Test Category",
        "is_custom": False,
    }
    response: Response = test_client.post(
        "/api/v1/products/",
        json=product_data,
    )

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["name"] == "Test Product"


def test_create_product_invalid_data(test_client: TestClient) -> None:
    invalid_product_data: dict[str, str] = {"name": "Invalid Product"}
    response: Response = test_client.post(
        "/api/v1/products/",
        json=invalid_product_data,
    )

    assert (
        response.status_code == 422
    )  # Unprocessable Entity due to missing required fields


def test_get_product_by_id(test_db: Session, test_client: TestClient) -> None:
    product: Product = create_product(
        test_db,
        ProductCreateSchema(
            name="Test Product",
            description="A sample product",
            category="Bicycle",
            base_price=100.0,
            is_custom=False,
        ),
    )
    response: Response = test_client.get(f"/api/v1/products/{product.id}")

    assert response.status_code == 200
    assert response.json()["id"] == str(product.id)
    assert response.json()["name"] == "Test Product"


def test_get_product_by_non_existent_id(test_client: TestClient) -> None:
    response: Response = test_client.get(f"/api/v1/products/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_get_all_products(test_db: Session, test_client: TestClient) -> None:
    create_product(
        test_db,
        ProductCreateSchema(
            name="Test Product 1",
            description="A sample product",
            category="Bicycle",
            base_price=100.0,
            is_custom=False,
        ),
    )
    create_product(
        test_db,
        ProductCreateSchema(
            name="Test Product 2",
            description="A sample product",
            category="Bicycle",
            base_price=100.0,
            is_custom=False,
        ),
    )

    response: Response = test_client.get("/api/v1/products/")
    assert response.status_code == 200

    products = response.json()
    assert len(products) >= 2


def test_update_product(test_db: Session, test_client: TestClient) -> None:
    product: Product = create_product(
        test_db,
        ProductCreateSchema(
            name="Test Product",
            description="A sample product",
            category="Bicycle",
            base_price=100.0,
            is_custom=False,
        ),
    )
    updated_data = {
        "name": "Updated Name",
        "base_price": 120.0,
    }
    response: Response = test_client.put(
        f"/api/v1/products/{product.id}",
        json=updated_data,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"
    assert response.json()["base_price"] == 120.0


def test_update_product_invalid_id(test_client: TestClient) -> None:
    updated_data = {
        "name": "Non Existent Product",
        "base_price": 150.0,
    }
    response: Response = test_client.put(
        f"/api/v1/products/{uuid4()}",
        json=updated_data,
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_delete_product(test_db: Session, test_client: TestClient) -> None:
    product: Product = create_product(
        test_db,
        ProductCreateSchema(
            name="Test Product",
            description="A sample product",
            category="Bicycle",
            base_price=100.0,
            is_custom=False,
        ),
    )
    response: Response = test_client.delete(f"/api/v1/products/{product.id}")

    assert response.status_code == 204
    assert response.text == ""


def test_delete_non_existent_product(test_client: TestClient) -> None:
    response: Response = test_client.delete(f"/api/v1/products/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
