from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

# Importamos la instancia de la Fachada de Aplicación creada explícitamente en app.py
from src.adapters.api.facade_instance import api_facade

# Creamos un router específico para rutas de salud/sistema
router = APIRouter(tags=["health"])


@router.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    """Endpoint básico para verificar que el servicio está funcionando."""
    project_name, environment = api_facade.health_check()
    return JSONResponse(
        content={"project_name": project_name, "environment": environment},
        status_code=status.HTTP_200_OK,
    )
