# Contenido para src/adapters/api/routes/status.py

from fastapi import APIRouter

# Importamos la instancia de la Fachada de Aplicación
from src.adapters.api.facade import api_facade

# Crea el router
router = APIRouter(tags=["status"])


@router.get("/status")
async def get_system_status_route():
    """
    Expone el estado de salud del sistema llamando a la Fachada de Aplicación.
    """
    # El adaptador llama a la Fachada de Aplicación, no directamente al Dominio.
    return api_facade.get_status()
