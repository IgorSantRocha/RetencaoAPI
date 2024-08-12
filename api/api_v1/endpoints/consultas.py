from typing import Any, List
import logging
from schemas.apikey_schema import APIKeyPerson
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from core.core_apikey import busca_meio_captura
from schemas.lista_projeto_schema import ListaProjetoBaseSC
from schemas.tb_projeto_fedex_schema import TbProjetoFedexSC, TbProjetoFedexConsultaOSSC
from schemas.ocorrencia_schema import ListaOcorrenciaBaseSC
from schemas.tipo_atendimento_schema import TipoAtendimentoBaseSC
from core.core_consultas import Consultas
from api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/projetos/", response_model=List[ListaProjetoBaseSC])
async def consulta_lista_projetos(
        db: Session = Depends(deps.get_db),
        cliente: str = None,
        api_key: APIKeyPerson = Depends(busca_meio_captura)
) -> Any:
    """
    Consulta projetos
    """
    consulta = Consultas()
    logger.info("Consultando projetos")
    return await consulta.busca_lista_projetos(cliente, db)


@router.get("/ocorrencias/", response_model=List[ListaOcorrenciaBaseSC])
async def consulta_lista_ocorrencias(
        db: Session = Depends(deps.get_db),
        projeto: str = Query(..., description="Nome do projeto"),
        api_key: APIKeyPerson = Depends(busca_meio_captura)
) -> Any:
    """
    Consulta projetos
    """
    consulta = Consultas()
    logger.info("Consultando projetos")
    return await consulta.busca_lista_ocorrencias(projeto, db)


@router.get("/tipos/", response_model=List[TipoAtendimentoBaseSC])
async def consulta_lista_tipos(
        db: Session = Depends(deps.get_db),
        projeto: str = Query(..., description="Nome do projeto"),
        api_key: APIKeyPerson = Depends(busca_meio_captura)
) -> Any:
    """
    Consulta projetos
    """
    consulta = Consultas()
    logger.info("Consultando projetos")
    return await consulta.busca_lista_tipos(projeto, db)


@router.get("/ordens-atendidas/{uid}", response_model=List[TbProjetoFedexSC])
async def consulta_ordens_atendidas_pelo_tec(
        uid: int = 0,
        db: Session = Depends(deps.get_db),
        api_key: APIKeyPerson = Depends(busca_meio_captura)
) -> Any:
    consulta = Consultas()
    logger.info("Consultando projetos")
    return await consulta.busca_lista_os_por_uid(uid=uid, db=db)


@router.get("/detalhes/os/{os}", response_model=TbProjetoFedexConsultaOSSC)
async def consulta_ordens_atendidas_pelo_tec(
        os: str,
        db: Session = Depends(deps.get_db),
        api_key: APIKeyPerson = Depends(busca_meio_captura)
) -> Any:
    """
    Consulta detalhes OS
    """
    consulta = Consultas()
    logger.info("Consultando projetos")
    return await consulta.busca_detalhes_os(db=db, os=os)
