"""Pytest configuration and shared fixtures."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app
from app.services.state_service import seed_initial_data


# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///./test_vari_os.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create tables and seed data once for all tests."""
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()
    yield
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    # Clean up test db file
    import os
    try:
        if os.path.exists("test_vari_os.db"):
            os.remove("test_vari_os.db")
    except PermissionError:
        pass  # Windows file lock; file will be cleaned up next run


@pytest.fixture()
def client(setup_database):
    """FastAPI test client with DB override."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def db_session(setup_database):
    """Direct DB session for unit tests."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
