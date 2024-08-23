from pydantic import BaseModel as SCBaseModel
from typing import Literal, Optional


class Sms(SCBaseModel):
    os: str
    telefone: str
    conclusao: str
    obs_atendente: str
