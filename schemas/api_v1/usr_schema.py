from pydantic import BaseModel


class UsrAgSC(BaseModel):
    usr: str
    nome: str
    id: int
    niveldescricao: str
    email: str


class UsrRetSC(BaseModel):
    usr: str
    nome: str
    pwd: str
    id: int
    nivel: str
