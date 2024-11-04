from typing import Optional
from pydantic import BaseModel, Field


class ListaProjetoBaseSC(BaseModel):
    projeto: str


class ListaProjetoCreateSC(ListaProjetoBaseSC):
    pass


class ListaProjetoUpdateSC(ListaProjetoBaseSC):
    pass


class ListaProjetoInDbBaseSC(ListaProjetoBaseSC):
    id: int
    fase: str
    cliente: str


class ListaProjetoSC(ListaProjetoInDbBaseSC):
    pass
