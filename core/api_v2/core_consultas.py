from sqlalchemy.ext.asyncio import AsyncSession
from schemas.api_v1.lista_projeto_schema import ListaProjetoBaseSC
from schemas.api_v1.tipo_atendimento_schema import TipoAtendimentoBaseSC
from schemas.api_v1.ocorrencia_schema import ListaOcorrenciaBaseSC
from schemas.api_v1.tb_projeto_fedex_schema import TbProjetoFedexSC, TbProjetoFedexConsultaOSSC
from crud.api_v1.crud_lista_projeto import lista_projetos
from crud.api_v1.crud_lista_ocorrencia import lista_ocorrencia
from crud.api_v1.crud_lista_tipo_atendimento import lista_tipo_atendimento
from crud.api_v1.crud_tb_projeto_fd import tb_projeto_fd
from fastapi import HTTPException
import re


class Consultas:
    async def busca_lista_os_por_uid(self, uid: int, db: AsyncSession, cliente: str) -> list[TbProjetoFedexSC]:
        consulta = tb_projeto_fd.get_recente(db=db, uid=uid, cliente=cliente)

        return consulta
