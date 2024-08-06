import logging
from fastapi import APIRouter, Depends, status
from schemas.auth_schema import Auth, AuthResponse, AuthCreate
from core.core_apikey import busca_meio_captura
from core.core_auth import AuthOdoo
from schemas.apikey_schema import APIKeyPerson
from api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/login/', response_model=AuthResponse, status_code=status.HTTP_200_OK,
             summary='Realiza o login',
             description='Loga o usuário e retorna o UID',
             response_description='Autenticado com sucesso')
async def post_login(auth_data: Auth,
                     api_key: APIKeyPerson = Depends(
                         busca_meio_captura)):
    logger.info("Autenticando usuário")
    auth = AuthOdoo()
    response: AuthResponse = await auth.autentica_usuario(
        usr=auth_data.username, pwd=auth_data.password)
    return response


@router.post('/create/', response_model=AuthResponse, status_code=status.HTTP_200_OK,
             summary='Cria o usuário',
             description='Cria o usuário com base nas informações passadas',
             response_description='Usuário criado')
async def post_create_user(auth_data: AuthCreate,
                           api_key: APIKeyPerson = Depends(
                               busca_meio_captura)):
    logger.info("Criando usuário")
    auth = AuthOdoo()
    response: AuthResponse = await auth.cria_usuario(new_usr=auth_data)
    return response
