from typing import Optional
from pydantic import BaseModel, Field


class ListaProjetoBaseSC(BaseModel):
    PROJETO: str


class ListaProjetoCreateSC(ListaProjetoBaseSC):
    pass


class ListaProjetoUpdateSC(ListaProjetoBaseSC):
    pass


class ListaProjetoInDbBaseSC(ListaProjetoBaseSC):
    id: int


class ListaProjetoSC(ListaProjetoInDbBaseSC):
    pass
