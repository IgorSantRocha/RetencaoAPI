from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TbProjetoFedexBaseSC(BaseModel):
    os: str
    problema_apresentado: str
    ocorrencia: str
    projeto: str
    tipo_atendimento: str
    # dt_abertura: Optional[datetime]
    dt_abertura: str
    atendente_abertura: str
    retorno_tecnico: str
    nome_tecnico: str
    telefone_tecnico: str
    acao_D29: str
    status: str
    subprojeto: str
    cliente: str
    versao: str
    chave: str
    # dt_fechamento: Optional[datetime]
    dt_fechamento: str
    fase: str
    conclusao_operador: str
    definicao: str
    status_relatorio: str
    etapa: str
    tipo: str
    acao_d1: str
    call_id: str
    reabertura: Optional[str]


class TbProjetoFedexCreateSC(TbProjetoFedexBaseSC):
    pass


class TbProjetoFedexUpdateSC(TbProjetoFedexBaseSC):
    pass


class TbProjetoFedexInDbBaseSC(TbProjetoFedexBaseSC):
    id: int


class TbProjetoFedexSC(TbProjetoFedexInDbBaseSC):
    pass
