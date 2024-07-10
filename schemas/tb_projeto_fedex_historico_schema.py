from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TbProjetoFedexHistoricoBaseSC(BaseModel):
    telefone_tecnico: Optional[str]
    os: str
    problema_apresentado: Optional[str]
    ocorrencia: Optional[str]
    projeto: Optional[str]
    tipo_atendimento: Optional[str]
    tecnico: Optional[str]


class TbProjetoFedexHistoricoCreateSC(TbProjetoFedexHistoricoBaseSC):
    pass


class TbProjetoFedexHistoricoUpdate(TbProjetoFedexHistoricoBaseSC):
    pass


class TbProjetoFedexHistoricoInDbBaseSC(TbProjetoFedexHistoricoBaseSC):
    id: int


class TbProjetoFedexHistoricoSC(TbProjetoFedexHistoricoInDbBaseSC):
    pass
