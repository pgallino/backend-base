from dataclasses import asdict

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.adapters.api.facade_instance import api_facade

router = APIRouter(tags=["herramientas"])  # Spanish path tag


class ToolCreateRequest(BaseModel):
    name: str
    description: str | None = None
    link: str | None = None


@router.post("/herramientas", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_tool_route(request: ToolCreateRequest):
    tool = await api_facade.create_tool(
        name=request.name,
        description=request.description or "",
        link=request.link or "",
    )
    return JSONResponse(content=asdict(tool), status_code=status.HTTP_201_CREATED)


@router.get(
    "/herramientas/{tool_id}", response_model=None, status_code=status.HTTP_200_OK
)
async def get_tool_route(tool_id: int):
    tool = await api_facade.get_tool(tool_id)
    if tool is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found"
        )
    return JSONResponse(content=asdict(tool), status_code=status.HTTP_200_OK)


@router.get("/herramientas", response_model=None, status_code=status.HTTP_200_OK)
async def list_tools_route():
    tools = await api_facade.list_tools()
    # tools is a list of dataclass Tool — convert to list of dicts
    content = [asdict(t) for t in tools]
    return JSONResponse(content=content, status_code=status.HTTP_200_OK)
