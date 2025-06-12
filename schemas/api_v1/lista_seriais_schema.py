from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ListaSeriaisBaseSC(BaseModel):
    serial: str
    os: str
    criadoem: str
    uid: int


class ListaSeriaisCreateSC(ListaSeriaisBaseSC):
    pass


class ListaSeriaisUpdateSC(ListaSeriaisBaseSC):
    pass


class ListaSeriaisInDbBaseSC(ListaSeriaisBaseSC):
    id: int
    serial: str
    os: str
    criadoem: datetime
    uid: int


class ListaSeriaisSC(ListaSeriaisInDbBaseSC):
    pass
