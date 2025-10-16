# Contenido para src/adapters/api/routes/status.py

from fastapi import APIRouter

# Importamos la instancia de la Fachada de Aplicación
from src.adapters.api.facade import api_facade

# Crea el router
router = APIRouter(tags=["user"])


@router.get("/user")
async def get_user_route():
    """
    Expone un perfil de usuario de ejemplo llamando a la Fachada de Aplicación.
    """
    return api_facade.get_user()
