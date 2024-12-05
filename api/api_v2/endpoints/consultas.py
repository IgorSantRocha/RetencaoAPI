from typing import Any, List
import logging
from schemas.api_v1.apikey_schema import APIKeyPerson
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from core.api_v1.core_apikey import busca_meio_captura
from schemas.api_v1.lista_projeto_schema import ListaProjetoBaseSC
from schemas.api_v1.tb_projeto_fedex_schema import TbProjetoFedexSC, TbProjetoFedexConsultaOSSC
from schemas.api_v1.ocorrencia_schema import ListaOcorrenciaBaseSC
from schemas.api_v1.tipo_atendimento_schema import TipoAtendimentoBaseSC
from core.api_v2.core_consultas import Consultas
from api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/ctbfed/ordens-atendidas/{uid}", response_model=List[TbProjetoFedexSC])
async def consulta_ordens_atendidas_pelo_tec(
        uid: int = 0,
        db: Session = Depends(deps.get_db),
        api_key: APIKeyPerson = Depends(busca_meio_captura)
) -> Any:
    consulta = Consultas()
    logger.info("Consultando OS's atendidas pelo tecnico de acordo com o APP")
    return await consulta.busca_lista_os_por_uid(uid=uid, db=db, cliente='CTBFED')


@router.get("/ctbseq/ordens-atendidas/{uid}", response_model=List[TbProjetoFedexSC])
async def consulta_ordens_atendidas_pelo_tec(
        uid: int = 0,
        db: Session = Depends(deps.get_db),
        api_key: APIKeyPerson = Depends(busca_meio_captura)
) -> Any:
    consulta = Consultas()
    logger.info("Consultando OS's atendidas pelo tecnico de acordo com o APP")
    return await consulta.busca_lista_os_por_uid(uid=uid, db=db, cliente='CTBSEQ')
