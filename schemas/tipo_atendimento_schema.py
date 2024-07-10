from typing import Optional
from pydantic import BaseModel, Field


class TipoAtendimentoBaseSC(BaseModel):
    Tipo_Atendimento: str


class TipoAtendimentoCreateSC(TipoAtendimentoBaseSC):
    pass


class TipoAtendimentoUpdateSC(TipoAtendimentoBaseSC):
    pass


class TipoAtendimentoInDbBaseSC(TipoAtendimentoBaseSC):
    id: int


class TipoAtendimentoSC(TipoAtendimentoInDbBaseSC):
    pass
