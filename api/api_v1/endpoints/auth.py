import logging
from fastapi import APIRouter, Depends, status
from schemas.auth_schema import Auth, AuthResponse, AuthCreate, AuthResetPassword
from schemas.auth_schema import AuthTokenVerficicacaoCreate, AuthTokenVerficicacaoResponse
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


@router.post('/reset_password/', response_model=dict(), status_code=status.HTTP_200_OK,
             summary='Altera a senha',
             description='Altera a senha do usuário especificado',
             response_description='Senha alterada com sucesso!')
async def post_reset_password(auth_data: AuthResetPassword,
                              api_key: APIKeyPerson = Depends(
                                  busca_meio_captura)):
    logger.info("Resetando senha do usuário")
    auth = AuthOdoo()
    response: AuthResetPassword = await auth.altera_senha(auth_data)
    return response


@router.post('/enviar_token/', response_model=AuthTokenVerficicacaoResponse, status_code=status.HTTP_200_OK,
             summary='Altera a senha',
             description='Altera a senha do usuário especificado',
             response_description='Senha alterada com sucesso!')
async def post_enviar_token(auth_data: AuthTokenVerficicacaoCreate,
                            api_key: APIKeyPerson = Depends(
                                busca_meio_captura)):
    logger.info("Gerando e enviando token")
    auth = AuthOdoo()
    response: AuthResetPassword = await auth.cria_token_verificacao(auth_data=auth_data)
    return response
