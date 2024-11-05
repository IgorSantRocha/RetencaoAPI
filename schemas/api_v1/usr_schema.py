from pydantic import BaseModel


class UsrBase(BaseModel):
    id: int
    usr: str
    nome: str
    pwd: str


class UsrAgSC(UsrBase):
    niveldescricao: str
    email: str


class UsrRetSC(UsrBase):
    nivel: str
