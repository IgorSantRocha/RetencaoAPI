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
