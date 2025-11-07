from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

# The facade is instantiated in `src.app` — import it at runtime in the handler

# Creamos un router específico para rutas de salud/sistema
router = APIRouter(tags=["health"])


@router.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    """Endpoint básico para verificar que el servicio está funcionando."""
    from src.application.api_app import api_facade

    project_name, environment = api_facade.health_check()
    return JSONResponse(
        content={"project_name": project_name, "environment": environment},
        status_code=status.HTTP_200_OK,
    )
