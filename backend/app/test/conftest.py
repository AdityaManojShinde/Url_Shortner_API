from fastapi.testclient import TestClient
import pytest
from app.main import app

@pytest.fixture(scope="session")
def client():
    """Shared TestClient instance for all tests"""
    return TestClient(app)