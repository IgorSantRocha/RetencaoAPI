from sqlalchemy.ext.asyncio import AsyncSession
from schemas.lista_projeto_schema import ListaProjetoBaseSC
from crud.crud_lista_projeto import lista_projetos
from crud.crud_lista_ocorrencia import lista_ocorrencia
from fastapi import HTTPException
import re


class Consultas:

    async def busca_lista_projetos(self, cliente: str, db: AsyncSession) -> list[ListaProjetoBaseSC]:
        filters_projeto = [
            {"field": "fase", "operator": "=", "value": "D+0"},
            {"field": "projeto", "operator": "!=", "value": "TESTE"}
        ]

        if cliente:
            cliente = self._valida_cliente(cliente)
            filters_projeto = filters_projeto.append(
                {"field": "cliente", "operator": "=", "value": cliente})

        projetos = lista_projetos.get_multi_filters(
            db=db, filters=filters_projeto)

        return projetos

    async def busca_lista_ocorrencias(self, projeto: str, db: AsyncSession) -> list[ListaProjetoBaseSC]:
        if projeto == 'FISERV':
            projeto = 'FIRST'

        self._valida_projeto(projeto, db)

        filters_ocorrencias = [
            {"field": "projeto", "operator": "=", "value": projeto},
            {"field": "motivo", "operator": "!=", "value": "..."}
        ]

        ocorrencias = lista_ocorrencia.get_multi_filters(
            db=db, filters=filters_ocorrencias)

        return ocorrencias

    ##### VALIDAÇÕES #####
    def _valida_cliente(self, cliente: str):
        pattern = re.compile(r"^CTB[A-Z]{3}$")
        if not pattern.match(cliente):
            raise HTTPException(
                status_code=400,
                detail="O valor do cliente deve começar com 'CTB' e ter exatamente 6 caracteres alfanuméricos."
            )
        return cliente.upper()

    def _valida_projeto(self, projeto: str, db: AsyncSession):
        projetos = lista_projetos.get_multi_filter(
            db=db, filterby='projeto', filter=projeto)
        if not projetos:
            raise HTTPException(
                status_code=404,
                detail=f'{projeto} não existe na lista de projetos!'
            )
