from fastapi import APIRouter

from api.api_v1.endpoints import consultas, abertura, auth, firebase, respostas_sga, base_cep

api_router = APIRouter()

api_router.include_router(
    base_cep.router, prefix="/busca-cep", tags=["Consultas CEP"])

api_router.include_router(
    auth.router, prefix="/auth", tags=["Autenticação"])

api_router.include_router(
    consultas.router, prefix="/consultas", tags=["Consultas V1"])

api_router.include_router(
    firebase.router, prefix="/firebase", tags=["Firebase Upload"])

api_router.include_router(
    abertura.router, prefix="/abertura", tags=["Abertura"])

api_router.include_router(
    respostas_sga.router, prefix="/respostas", tags=["Respostas SGA"])
