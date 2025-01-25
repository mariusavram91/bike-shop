# tests/conftest.py

from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy import Engine
from sqlalchemy.pool import StaticPool


# Use an in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"

engine: Engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture
def test_db() -> Generator[Session, Any, None]:
    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session
    session.close()

    SQLModel.metadata.drop_all(bind=engine)


@pytest.fixture
def test_client(test_db: Session) -> Generator[TestClient, Any, None]:
    from app.database import get_session
    from app.main import app

    def override_get_session() -> Generator[Session, Any, None]:
        yield test_db

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client
