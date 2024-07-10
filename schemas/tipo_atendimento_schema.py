from typing import Optional
from pydantic import BaseModel, Field


class TipoAtendimentoBase(BaseModel):
    Tipo_Atendimento: str


class TipoAtendimentoCreate(TipoAtendimentoBase):
    pass


class TipoAtendimentoUpdate(TipoAtendimentoBase):
    pass


class TipoAtendimentoInDbBase(TipoAtendimentoBase):
    id: int


class TipoAtendimento(TipoAtendimentoInDbBase):
    pass
