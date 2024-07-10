from typing import Optional
from pydantic import BaseModel, Field


class ListaOcorrenciaBase(BaseModel):
    motivo: str


class ListaOcorrenciaCreate(ListaOcorrenciaBase):
    pass


class ListaOcorrenciaUpdate(ListaOcorrenciaBase):
    pass


class ListaOcorrenciaInDbBase(ListaOcorrenciaBase):
    id: int


class ListaOcorrencia(ListaOcorrenciaInDbBase):
    pass
