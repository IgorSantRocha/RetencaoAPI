import logging
from fastapi import APIRouter, Depends, status
from schemas.api_v1.auth_schema import Auth, AuthResponse, AuthCreate, AuthResetPassword, AuthTokenValidacao, AuthAlterCadUser
from schemas.api_v1.auth_schema import AuthTokenVerficicacaoCreate, AuthTokenVerficicacaoResponse, AuthTokenValidacaoResponse, AuthTokenVerficicacaoSolic
from schemas.api_v1.usr_schema import UserGeralSC
from core.api_v1.core_apikey import busca_meio_captura
from core.api_v1.core_auth import AuthOdoo, Auth2Factores
from schemas.api_v1.apikey_schema import APIKeyPerson
from api import deps
from sqlalchemy.orm import Session

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


@router.get('/info_verificacao/{username}', response_model=AuthTokenVerficicacaoSolic, status_code=status.HTTP_200_OK,
            summary='Retorna o telefone e e-mail',
            description='Retorna o telefone e e-mail pelo username para ser usado na verificação'
            )
async def get_info_verificacao(username: str,
                               api_key: APIKeyPerson = Depends(
                                   busca_meio_captura)):
    logger.info("Gerando e enviando token")
    auth = AuthOdoo()
    response: AuthTokenValidacaoResponse = await auth.busca_info_verificacao(username)
    return response


@router.post('/enviar_token/', response_model=AuthTokenVerficicacaoResponse, status_code=status.HTTP_200_OK,
             summary='Cria e envia o Token',
             description='Cria o Token e envia através do método escolhido',
             response_description='Senha alterada com sucesso!')
async def post_enviar_token(auth_data: AuthTokenVerficicacaoCreate,
                            api_key: APIKeyPerson = Depends(
                                busca_meio_captura)):
    logger.info("Gerando e enviando token")
    auth = AuthOdoo()
    response: AuthResetPassword = await auth.cria_token_verificacao(auth_data=auth_data)
    return response


@router.post('/validar_token/', response_model=AuthTokenValidacaoResponse, status_code=status.HTTP_200_OK,
             summary='Validar Token',
             description='Valida o Token e retorna o UID do usuário.',
             response_description='Senha alterada com sucesso!')
async def post_validar_token(auth_data: AuthTokenValidacao,
                             api_key: APIKeyPerson = Depends(
                                 busca_meio_captura)):
    logger.info("Gerando e enviando token")
    auth = AuthOdoo()
    response: AuthTokenValidacaoResponse = await auth.valida_token_verificacao(auth_data)
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


@router.post('/alter_cad/', response_model=AuthAlterCadUser, status_code=status.HTTP_200_OK,
             summary='Altera cadastro',
             description='Altera o cadastro do usuário',
             response_description='Cadastro alterado com sucesso!')
async def post_alter_cad(auth_data: AuthAlterCadUser,
                         api_key: APIKeyPerson = Depends(
                             busca_meio_captura)):
    logger.info("Alterando cadastro do usuário")
    auth = AuthOdoo()
    response: AuthResetPassword = await auth.altera_cadastro(auth_data)
    return response


@router.post('/delete/', response_model=int, status_code=status.HTTP_200_OK,
             summary='Deleta o usuário',
             description='Deleta o usuário e todas as dependencias',
             response_description='Usuário deletado')
async def post_delete(auth_data: Auth,
                      api_key: APIKeyPerson = Depends(
                          busca_meio_captura)):
    logger.info("Deletando usuário")
    auth = AuthOdoo()
    response: AuthResponse = await auth.deleta_usuario(
        usr=auth_data.username, pwd=auth_data.password)
    return response


@router.post('/login2factores/', response_model=dict(), status_code=status.HTTP_200_OK,
             summary='Realiza o login 2 fatores',
             description='Loga o usuário e manda o token de verificação no e-mail',
             response_description='Token enviado com sucesso')
async def post_login2factores(auth_data: Auth,
                              api_key: APIKeyPerson = Depends(
                                  busca_meio_captura),
                              db_212: Session = Depends(deps.get_db),
                              db_211: Session = Depends(deps.get_db_211)):
    logger.info("Autenticando usuário")
    auth = Auth2Factores()
    response = await auth.verifica_credenciais(
        usr=auth_data.username, pwd=auth_data.password, db_211=db_211, db_212=db_212)

    return {'msg': 'Token de validação enviado no e-mail'}


@router.post('/validar_token2factores/', response_model=UserGeralSC, status_code=status.HTTP_200_OK,
             summary='Validar Token',
             description='Valida o Token e retorna as informações do usuário.',
             response_description='Usuário logado com sucesso!')
async def post_validar_token_2factores(auth_data: AuthTokenValidacao,
                                       api_key: APIKeyPerson = Depends(
                                           busca_meio_captura),
                                       db_211: Session = Depends(
                                           deps.get_db_211),
                                       db_212: Session = Depends(deps.get_db)):

    logger.info("Validando token")
    auth = Auth2Factores()
    response: UserGeralSC = await auth.valida_token(db_211=db_211, db_212=db_212, usr=auth_data.username, token=auth_data.token)
    return response
