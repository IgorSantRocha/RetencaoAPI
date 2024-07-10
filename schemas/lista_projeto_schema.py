from typing import Optional
from pydantic import BaseModel, Field


class ListaProjetoBaseSC(BaseModel):
    projeto: str
    fase: str
    cliente: str


class ListaProjetoCreateSC(ListaProjetoBaseSC):
    pass


class ListaProjetoUpdateSC(ListaProjetoBaseSC):
    pass


class ListaProjetoInDbBaseSC(ListaProjetoBaseSC):
    id: int


class ListaProjetoSC(ListaProjetoInDbBaseSC):
    pass
