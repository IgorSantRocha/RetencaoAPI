from pydantic import BaseModel as SCBaseModel
from typing import Literal, Optional


class Sms(SCBaseModel):
    os: str
    telefone: str
    codigo_conclusao: str
    obs_atendente: str
    protocolo: str
