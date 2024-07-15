from typing import Annotated, Union
import logging
from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from schemas.tb_projeto_fedex_historico_schema import TbProjetoFedexHistoricoBaseSC
from schemas.tb_projeto_fedex_schema import TbProjetoFedexCreateSC
from core.core_tokens import Token
from core.core_abertura import Abertura
from api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/abertura/', response_model=TbProjetoFedexCreateSC, status_code=status.HTTP_202_ACCEPTED,
             summary='Realiza a abertura da OS',
             description='Realiza a abertura/reabertura da OS verificando se a OS existeou não e então decidindo entre update/insert',
             response_description='Abertura realizada!')
async def post_abertura_chatbot(info_os: TbProjetoFedexHistoricoBaseSC,
                                apikey: Annotated[Union[str, None], Header()],
                                db: Session = Depends(deps.get_db)):
    logger.info("iniciando abertura do chamado")
    validacao = Token()
    meio_captura = await validacao.valida_token(apikey=apikey, db=db)
    abertura = Abertura()

    return await abertura.abertura_os(info_os=info_os, meio_captura=meio_captura, db=db)
