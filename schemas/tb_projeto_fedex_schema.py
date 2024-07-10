from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TbProjetoFedexBaseSC(BaseModel):
    os: str
    problema_apresentado: Optional[str]
    ocorrencia: Optional[str]
    projeto: Optional[str]
    tipo_atendimento: Optional[str]
    dt_abertura: Optional[datetime]
    atendente_abertura: Optional[str]
    retorno_tecnico: Optional[str]
    nome_tecnico: Optional[str]
    telefone_tecnico: Optional[str]
    acao_D29: Optional[str]
    status: Optional[str]
    subprojeto: Optional[str]
    cliente: Optional[str]
    versao: Optional[str]
    chave: Optional[str]
    dt_fechamento: Optional[datetime]
    fase: Optional[str]
    conclusao_operador: Optional[str]
    definicao: Optional[str]
    status_relatorio: Optional[str]
    etapa: Optional[str]
    tipo: Optional[str]
    acao_d1: Optional[str]


class TbProjetoFedexCreateSC(TbProjetoFedexBaseSC):
    pass


class TbProjetoFedexUpdateSC(TbProjetoFedexBaseSC):
    pass


class TbProjetoFedexInDbBaseSC(TbProjetoFedexBaseSC):
    id: int


class TbProjetoFedexSC(TbProjetoFedexInDbBaseSC):
    pass
