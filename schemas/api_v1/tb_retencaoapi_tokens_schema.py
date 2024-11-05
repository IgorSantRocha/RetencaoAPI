from datetime import datetime
from pydantic import BaseModel


class RetencaoAPITokensBaseSC(BaseModel):
    apikey: str
    nome: str
    list_permissions: str


class RetencaoAPITokensCreateSC(RetencaoAPITokensBaseSC):
    pass


class RetencaoAPITokensUpdateSC(RetencaoAPITokensBaseSC):
    pass


class RetencaoAPITokensInDbBaseSC(RetencaoAPITokensBaseSC):
    id: int


class RetencaoAPITokensSC(RetencaoAPITokensInDbBaseSC):
    pass


class APITokensBaseSC(BaseModel):
    id: int
    criadoem: datetime
    usr: str
    token: str
    expiraem: datetime
    usado: bool


class APITokensCreateSC(BaseModel):
    usr: str
    token: int


class APITokensUpdateSC(BaseModel):
    id: int
    usado: bool
