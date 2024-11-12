from pydantic import BaseModel


class UsrBase(BaseModel):
    id: int
    usr: str
    nome: str


class UsrAgSC(UsrBase):
    niveldescricao: str
    nivel: str
    email: str
    pwd: str


class UsrRetSC(UsrBase):
    nivel: str
    pwd: str


class UserGeralSC(UsrBase):
    niveldescricao: str
    nivel: int
