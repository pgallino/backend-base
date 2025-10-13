from fastapi import APIRouter

# Creamos un router específico para rutas de salud/sistema
router = APIRouter(tags=["health"])


@router.get("/")
async def health_check():
    """Endpoint básico para verificar que el servicio está funcionando."""
    return {"message": "Hello from BackendBase! The service is running."}
