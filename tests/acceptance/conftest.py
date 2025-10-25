import pytest
from sqlalchemy import create_engine, text
from fastapi.testclient import TestClient
from src.app import app


# Limpia la base antes de cada test de aceptación
@pytest.fixture(autouse=True)
def clean_db():
    engine = create_engine("sqlite:///dev.db")
    with engine.connect() as conn:
        # limpiar tablas existentes (user y tool si existen)
        try:
            conn.execute(text("DELETE FROM user"))
        except Exception:
            pass
        try:
            conn.execute(text("DELETE FROM tool"))
        except Exception:
            pass
        conn.commit()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def context():
    return {}
