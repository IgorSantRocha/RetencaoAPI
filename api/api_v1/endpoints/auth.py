from typing import Annotated, Union
import logging
from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from schemas.tb_projeto_fedex_historico_schema import TbProjetoFedexHistoricoBaseSC
from schemas.auth_schema import Auth
from core.core_apikey import get_api_key, busca_meio_captura
from core.core_abertura import Abertura
from fastapi.security.api_key import APIKey
from api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/login/', response_model=int, status_code=status.HTTP_200_OK,
             summary='Realiza o login',
             description='Loga o usuário e retorna o UID',
             response_description='Authentication successful')
async def post_abertura_chatbot(auth_data: Auth,
                                api_key: APIKey = Depends(get_api_key),
                                db: Session = Depends(deps.get_db)):
    logger.info("iniciando abertura do chamado")

    return 'OK'
