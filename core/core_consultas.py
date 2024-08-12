from sqlalchemy.ext.asyncio import AsyncSession
from schemas.lista_projeto_schema import ListaProjetoBaseSC
from schemas.tipo_atendimento_schema import TipoAtendimentoBaseSC
from schemas.ocorrencia_schema import ListaOcorrenciaBaseSC
from schemas.tb_projeto_fedex_schema import TbProjetoFedexSC, TbProjetoFedexConsultaOSSC
from crud.crud_lista_projeto import lista_projetos
from crud.crud_lista_ocorrencia import lista_ocorrencia
from crud.crud_lista_tipo_atendimento import lista_tipo_atendimento
from crud.crud_tb_projeto_fd import tb_projeto_fd
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
            filters_projeto.append(
                {"field": "cliente", "operator": "=", "value": cliente})

        projetos = lista_projetos.get_multi_filters(
            db=db, filters=filters_projeto)

        return projetos

    async def busca_lista_ocorrencias(self, projeto: str, db: AsyncSession) -> list[ListaOcorrenciaBaseSC]:
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

    async def busca_lista_tipos(self, projeto: str, db: AsyncSession) -> list[TipoAtendimentoBaseSC]:
        if projeto not in ('CTB', 'CTBPO', 'CIELO'):
            tipos = lista_tipo_atendimento.get_multi(db=db)
        else:
            tipos = lista_tipo_atendimento.get_multi_filter(
                db=db, filterby='Tipo_Atendimento', filter='Desinstalação')

        return tipos

    async def busca_lista_os_por_uid(self, uid: int, db: AsyncSession) -> list[TbProjetoFedexSC]:
        consulta = tb_projeto_fd.get_recente(db=db, uid=uid)

        return consulta

    async def busca_detalhes_os(self, os: str, db: AsyncSession) -> TbProjetoFedexConsultaOSSC:
        detalhes: TbProjetoFedexConsultaOSSC = tb_projeto_fd.get_first_by_filter(
            db=db, filterby='os', filter=os)

        return detalhes

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
