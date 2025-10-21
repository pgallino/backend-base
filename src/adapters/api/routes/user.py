# Contenido para src/adapters/api/routes/status.py

from dataclasses import asdict

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Importamos la instancia de la Fachada de Aplicación creada explícitamente en app.py
from src.adapters.api.facade_instance import api_facade

# Crea el router
router = APIRouter(tags=["user"])


class UserCreateRequest(BaseModel):
    username: str
    name: str
    email: str


@router.get("/user/{user_id}", response_model=None, status_code=status.HTTP_200_OK)
async def get_user_route(user_id: int):
    """
    Expone un perfil de usuario llamando a la Fachada de Aplicación y la base de datos.
    """
    user = await api_facade.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return JSONResponse(content=asdict(user), status_code=status.HTTP_200_OK)


@router.post("/user", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_user_route(request: UserCreateRequest):
    """
    Crea un usuario en la base de datos.
    """
    user = await api_facade.create_user(
        username=request.username,
        name=request.name,
        email=request.email,
    )
    return JSONResponse(content=asdict(user), status_code=status.HTTP_201_CREATED)
