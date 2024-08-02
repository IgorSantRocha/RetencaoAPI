from fastapi import APIRouter

from api.api_v1.endpoints import consultas, abertura, auth

api_router = APIRouter()
api_router.include_router(
    consultas.router, prefix="/consultas", tags=["Consultas"])

api_router.include_router(
    abertura.router, prefix="/abertura", tags=["Abertura"])

api_router.include_router(
    auth.router, prefix="/auth", tags=["Autenticação"])
