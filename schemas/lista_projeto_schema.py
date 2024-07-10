from typing import Optional
from pydantic import BaseModel, Field


class ListaProjetoBase(BaseModel):
    PROJETO: str


class ListaProjetoCreate(ListaProjetoBase):
    pass


class ListaProjetoUpdate(ListaProjetoBase):
    pass


class ListaProjetoInDbBase(ListaProjetoBase):
    id: int


class ListaProjeto(ListaProjetoInDbBase):
    pass
