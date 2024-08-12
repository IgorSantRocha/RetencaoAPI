from pydantic import BaseModel


class TipoAtendimentoBaseSC(BaseModel):
    Tipo_Atendimento: str


class TipoAtendimentoCreateSC(TipoAtendimentoBaseSC):
    pass


class TipoAtendimentoUpdateSC(TipoAtendimentoBaseSC):
    pass


class TipoAtendimentoInDbBaseSC(TipoAtendimentoBaseSC):
    id: int


class TipoAtendimentoSC(TipoAtendimentoInDbBaseSC):
    pass
