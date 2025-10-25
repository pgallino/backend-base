import pytest
from sqlalchemy import create_engine, text
from fastapi.testclient import TestClient
from src.app import app
from src.adapters.db.models.models import Base


# Limpia la base antes de cada test de aceptación
@pytest.fixture(autouse=True)
def clean_db():
    engine = create_engine("sqlite:///dev.db")
    # Ensure tables exist (helpful when running tests without running alembic)
    try:
        Base.metadata.create_all(engine)
    except Exception:
        pass

    with engine.connect() as conn:
        # Borra todas las filas de todas las tablas gestionadas por el modelo
        # excepto la tabla de alembic (si existe). Usamos sorted_tables para
        # respetar orden de dependencias (FKs) al borrar.
        for table in reversed(Base.metadata.sorted_tables):
            name = table.name
            if name == "alembic_version":
                continue
            try:
                conn.execute(text(f"DELETE FROM {name}"))
            except Exception:
                # Ignorar cualquier tabla que no exista o error puntual
                pass
        # Reset SQLite autoincrement sequences so IDs start from 1 in tests
        try:
            if engine.dialect.name == "sqlite":
                for table in Base.metadata.sorted_tables:
                    tname = table.name
                    if tname == "alembic_version":
                        continue
                    try:
                        conn.execute(text(f"DELETE FROM sqlite_sequence WHERE name='{tname}'"))
                    except Exception:
                        pass
        except Exception:
            # If dialect introspection fails or not sqlite, ignore
            pass
        conn.commit()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def context():
    return {}
