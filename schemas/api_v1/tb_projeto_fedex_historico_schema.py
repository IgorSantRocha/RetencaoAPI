from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class TbProjetoFedexHistoricoBaseSC(BaseModel):
    os: str
    problema_apresentado: Optional[str]
    tecnico: Optional[str]
    callid: Optional[str]


class TbProjetoFedexHistoricoCreateSC(TbProjetoFedexHistoricoBaseSC):
    pass


class TbProjetoFedexHistoricoUpdate(BaseModel):
    os: str
    ip: str


class TbProjetoFedexHistoricoInDbBaseSC(TbProjetoFedexHistoricoBaseSC):
    id: int


class TbProjetoFedexHistoricoSC(BaseModel):
    telefone_tecnico: Optional[str]
    oss: List[str]
    problema_apresentado: Optional[str]
    ocorrencia: Optional[str]
    projeto: Optional[str]
    tipo_atendimento: Optional[str]
    tecnico: Optional[str]
    unidade: Optional[str]
    uid: Optional[int]
    longitude: Optional[str]
    latitude: Optional[str]
    imageurl: Optional[str]
    seriais: List[Optional[str]] = None
