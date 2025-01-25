# app/database.py

from typing import Any, Generator

from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

from app.config import settings

if settings.DATABASE_URL.startswith("sqlite"):
    engine: Engine = create_engine(
        settings.DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False},
    )
else:
    engine: Engine = create_engine(
        settings.DATABASE_URL,
        echo=True,
    )


def create_db_and_tables() -> None:
    """
    Create the database and tables.

    This function initializes the database by creating all the tables
    defined in the SQLModel models.

    Args:
        None

    Returns:
        None
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, Any, None]:
    """
    Get a new database session.

    This creates a new SQLAlchemy session from the database engine.
    The session is used for interacting with the database and the
    session is automatically closed after the operation is complete.

    Yields:
        Session: A new SQLAlchemy session that can be used for querying or
        modifying the database.

    Example:
        ```python
        with get_session() as session:
            # Perform database operations
        ```
    """
    with Session(engine) as session:
        yield session
