from fastapi import APIRouter

# Importamos la instancia de la Fachada de Aplicación
from src.adapters.api.facade import api_facade

# Creamos un router específico para rutas de salud/sistema
router = APIRouter(tags=["health"])


@router.get("/")
async def health_check():
    """Endpoint básico para verificar que el servicio está funcionando."""
    return api_facade.health_check()
