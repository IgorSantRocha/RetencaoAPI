from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TbFedexFotosBaseSC(BaseModel):
    os: str
    latitude: str
    longitude: str
    imageurl: str
    uid: int
    data_abertura: str


class TbFedexFotosCreateSC(TbFedexFotosBaseSC):
    pass


class TbFedexFotosUploadSC(BaseModel):
    os: str
    latitude: str
    longitude: str
    uid: int


class TbFedexFotosUpdate(TbFedexFotosBaseSC):
    pass


class TbFedexFotosInDbBaseSC(TbFedexFotosBaseSC):
    id: int


class TbFedexFotosSC(BaseModel):
    data_abertura: datetime
    os: str
    latitude: str
    longitude: str
    imageurl: str
    uid: int
