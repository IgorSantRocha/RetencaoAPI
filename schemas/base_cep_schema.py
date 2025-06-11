from pydantic import BaseModel


class BaseCepBaseSC(BaseModel):
    cep: str
    id: int
    tipo: str
    logradouro: str
    logradouro_sem_numero: str
    complemento: str
    bairro: str
    cidade: str
    uf: str
    codigo_cidade_ibge: int


class BaseCepCreateSC(BaseCepBaseSC):
    pass


class BaseCepUpdateSC(BaseCepBaseSC):
    pass


class BaseCepInDbBaseSC(BaseCepBaseSC):
    pass


class BaseCepSC(BaseCepInDbBaseSC):
    pass
