from typing import Any, List
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.request import RequestClient
from schemas.lista_projeto_schema import ListaProjetoSC
from core.core_consultas import Consultas
from api import deps

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/projetos/", response_model=List[ListaProjetoSC])
async def consulta_lista_projetos(
        db: Session = Depends(deps.get_db),
        cliente: str = 'CTBFULL'
) -> Any:
    """
    Consulta projetos
    """
    consulta = Consultas()
    logger.info("Consultando projetos")
    return await consulta.busca_lista_projetos(cliente, db)
