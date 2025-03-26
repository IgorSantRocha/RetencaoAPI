from typing import Any, List
import logging
from schemas.api_v1.apikey_schema import APIKeyPerson
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from core.api_v1.core_apikey import busca_meio_captura

from schemas.api_v1.tb_fedex_fotos_schema import TbFedexFotosBaseConsultaSC
from schemas.api_v1.tb_projeto_fedex_schema import TbProjetoFedexSC

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


@router.get("/fotos_e_geo/os/{os}", response_model=List[TbFedexFotosBaseConsultaSC])
async def consulta_ordens_atendidas_pelo_tec(
        os: str,
        db: Session = Depends(deps.get_db),
        api_key: APIKeyPerson = Depends(busca_meio_captura)
) -> Any:
    """
    Consulta Fotos e Geo
    """
    consulta = Consultas()
    logger.info("Consultando projetos")
    return await consulta.busca_fotos_e_geo_os(db=db, os=os)
