from pydantic import BaseModel as SCBaseModel


class Auth(SCBaseModel):
    username: str
    password: str


class AuthResponse(SCBaseModel):
    uid: int
    username: str
    name: str
    phone: str
    email: str
    cod_base: str


class AuthCreate(SCBaseModel):
    username: str
    pwd: str
    pwd_confirm: str
    name: str
    phone: str
    email: str
    cod_base: str
