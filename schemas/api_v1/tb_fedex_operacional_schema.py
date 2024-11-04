from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TbFedexOpBaseSC(BaseModel):
    id: int
    codigo: str
    protocolo: bool
