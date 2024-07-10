from typing import Any, List
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.request import RequestClient
from schemas.lista_projeto_schema import ListaProjetoBaseSC
from schemas.ocorrencia_schema import ListaOcorrenciaBaseSC
from core.core_consultas import Consultas
from api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/projetos/", response_model=List[ListaProjetoBaseSC])
async def consulta_lista_projetos(
        db: Session = Depends(deps.get_db),
        cliente: str = None
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
        projeto: str = Query(..., description="Nome do projeto")
) -> Any:
    """
    Consulta projetos
    """
    consulta = Consultas()
    logger.info("Consultando projetos")
    return await consulta.busca_lista_ocorrencias(projeto, db)
