from fastapi import APIRouter

from api.api_v1.endpoints import consultas

api_router = APIRouter()
api_router.include_router(
    consultas.router, prefix="/consultas", tags=["Consultas"])
