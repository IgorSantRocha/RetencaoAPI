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
