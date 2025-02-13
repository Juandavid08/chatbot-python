import sys # importamos sys para poder importar los modulos de la carpeta principal
import os # importamos os para poder importar los modulos de la carpeta principal
import pytest # importamos pytest para poder hacer los test
from fastapi.testclient import TestClient
from main import app
from sqlmodel import Session, select
from database import engine
from models import User #   importamos el modelo User para poder hacer las consultas a la base de datos


# Agregamos la carpeta principal al path para poder importar los modulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

client = TestClient(app)

# Creamos un fixture para poder hacer las pruebas de los endpoints
@pytest.fixture(scope="function")
def session():
    with Session(engine) as session:
        yield session


# Test N1 de los endpoints, probamos que el endpoint de creacion de usuario funcione correctamente
def test_create_user(session):
    response = client.post("/init_user", json={"username": "maria", "role": "admin"})
    assert response.status_code == 200


# Test N2 de los endpoints, probamos que el endpoint de validacion de estado funcione correctamente
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
