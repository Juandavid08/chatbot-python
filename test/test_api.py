import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from main import app
from sqlmodel import Session, select
from database import engine
from models import User


client = TestClient(app)

@pytest.fixture(scope="function")
def session():
    with Session(engine) as session:
        yield session


def test_create_user(session):
    response = client.post("/init_user", json={"username": "maria", "role": "admin"})
    assert response.status_code == 200


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
