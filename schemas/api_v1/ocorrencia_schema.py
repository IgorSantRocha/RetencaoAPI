from typing import Optional
from pydantic import BaseModel, Field


class ListaOcorrenciaBaseSC(BaseModel):
    motivo: str


class ListaOcorrenciaCreateSC(ListaOcorrenciaBaseSC):
    pass


class ListaOcorrenciaUpdateSC(ListaOcorrenciaBaseSC):
    pass


class ListaOcorrenciaInDbBaseSC(ListaOcorrenciaBaseSC):
    id: int


class ListaOcorrenciaSC(ListaOcorrenciaInDbBaseSC):
    pass
