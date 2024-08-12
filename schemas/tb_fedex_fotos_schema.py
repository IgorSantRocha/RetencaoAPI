from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TbFedexFotosBaseSC(BaseModel):
    # data_abertura: datetime
    os: str
    longitude: str
    latitude: str
    imageurl: str
    uid: int


class TbFedexFotosCreateSC(TbFedexFotosBaseSC):
    pass


class TbFedexFotosUpdate(TbFedexFotosBaseSC):
    pass


class TbFedexFotosInDbBaseSC(TbFedexFotosBaseSC):
    id: int


class TbProjetoFedexHistoricoSC(BaseModel):
    data_abertura: datetime
    os: str
    longitude: str
    latitude: str
    imageurl: str
    uid: int
