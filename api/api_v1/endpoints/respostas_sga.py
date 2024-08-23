import logging
from schemas.apikey_schema import APIKeyPerson
from schemas.resposta_evolution_schema import MessageSchema
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.resposta_sms_schema import Sms
from schemas.resposta_evolution_schema import ResponseEvolutionSC
from core.core_apikey import busca_meio_captura
from core.core_respostas import RespostaSMS, RespostaWPP

from api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/SMS/', response_model=str, status_code=status.HTTP_202_ACCEPTED,
             summary='Envia resposta 0800',
             description='Envia resposta do 0800 via SMS',
             response_description='Mensagem enviada!')
async def post_resposta_sms(sms_data: Sms,
                            api_key: APIKeyPerson = Depends(
                                busca_meio_captura)):
    logger.info("iniciando envio da resposta")

    # meio_captura = api_key.meio_abertura
    resposta = RespostaSMS()

    return await resposta.enviar(sms_data)


@router.post('/WPP/', response_model=ResponseEvolutionSC, status_code=status.HTTP_202_ACCEPTED,
             summary='Envia resposta chatbot',
             description='Envia resposta do chatbot via WPP',
             response_description='Mensagem enviada!')
async def post_resposta_sms(wpp_data: MessageSchema,
                            db: Session = Depends(deps.get_db),
                            api_key: APIKeyPerson = Depends(
                                busca_meio_captura)):
    logger.info("iniciando envio da resposta")

    # meio_captura = api_key.meio_abertura
    resposta = RespostaWPP()

    return await resposta.enviar(db=db, info_messagem=wpp_data)
