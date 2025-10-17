from fastapi import APIRouter

# Importamos la instancia de la Fachada de Aplicación
from src.adapters.api.facade import api_facade

# Creamos un router específico para rutas de salud/sistema
router = APIRouter(tags=["aws"])


@router.get("/aws")
async def aws_check():
    """Endpoint básico para verificar que el servicio está funcionando en aws."""
    return api_facade.aws_check()
