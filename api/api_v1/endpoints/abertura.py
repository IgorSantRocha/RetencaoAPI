from typing import Any, List
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from core.request import RequestClient
from schemas.lista_projeto_schema import ListaProjetoBaseSC
from schemas.ocorrencia_schema import ListaOcorrenciaBaseSC
from schemas.tipo_atendimento_schema import TipoAtendimentoBaseSC
from schemas.tb_projeto_fedex_historico_schema import TbProjetoFedexHistoricoBaseSC
from schemas.tb_projeto_fedex_schema import TbProjetoFedexCreateSC
from core.core_consultas import Consultas
from core.core_abertura import Abertura
from api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.put('/abertura/{meio_captura}', response_model=TbProjetoFedexCreateSC, status_code=status.HTTP_202_ACCEPTED,
            summary='Realiza a abertura da OS',
            description='Realiza a abertura/reabertura da OS verificando se a OS existeou não e então decidindo entre update/insert',
            response_description='Abertura realizada!')
async def put_abertura_chatbot(info_os: TbProjetoFedexHistoricoBaseSC,
                               meio_captura: str,
                               db: Session = Depends(deps.get_db)):
    logger.info("iniciando abertura do chamado")
    abertura = Abertura()

    return await abertura.abertura_os(info_os=info_os, meio_captura=meio_captura, db=db)
