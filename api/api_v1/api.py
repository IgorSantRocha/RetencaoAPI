from fastapi import APIRouter

from api.api_v1.endpoints import consultas, abertura, auth, firebase, respostas_sga

api_router = APIRouter()
api_router.include_router(
    consultas.router, prefix="/consultas", tags=["Consultas"])

api_router.include_router(
    abertura.router, prefix="/abertura", tags=["Abertura"])

api_router.include_router(
    auth.router, prefix="/auth", tags=["Autenticação"])

api_router.include_router(
    firebase.router, prefix="/firebase", tags=["Firebase Upload"])

api_router.include_router(
    respostas_sga.router, prefix="/respostas", tags=["Respostas SGA"])
