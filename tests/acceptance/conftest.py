import pytest
from sqlalchemy import create_engine, text

# Limpia la base antes de cada test de aceptación
@pytest.fixture(autouse=True)
def clean_db():
    engine = create_engine("sqlite:///dev.db")
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM user"))
        conn.commit()
