import logging
from schemas.api_v1.apikey_schema import APIKeyPerson
from schemas.api_v1.resposta_evolution_schema import MessageSchema
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.api_v1.resposta_sms_schema import Sms
from schemas.api_v1.resposta_evolution_schema import ResponseEvolutionSC
from core.api_v1.core_apikey import busca_meio_captura
from core.api_v1.core_respostas import RespostaSMS, RespostaWPP
from crud.api_v1.crud_base_cep import crud_base_cep
from schemas.base_cep_schema import BaseCepSC

from api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/{cep}/json/', response_model=BaseCepSC, status_code=status.HTTP_200_OK,
            summary='Consulta a base de CEP',
            description='Faz a consulta do CEP direto na base C-Trends',
            response_description='Consulta realizada com sucesso!')
async def post_resposta_sms(cep: str,
                            db: Session = Depends(deps.get_db_211)):
    logger.info("iniciando consulta")

    # meio_captura = api_key.meio_abertura
    resposta = crud_base_cep.get_first_by_filter(
        db=db, filterby='cep', filter=cep)

    return resposta
