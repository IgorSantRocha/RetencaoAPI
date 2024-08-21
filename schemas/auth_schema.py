from pydantic import BaseModel as SCBaseModel
from typing import Literal, Optional


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
    documento: str


class AuthCreate(SCBaseModel):
    username: str
    pwd: str
    pwd_confirm: str
    name: str
    phone: str
    email: str
    cod_base: str
    documento: str


class AuthResetPassword(SCBaseModel):
    uid: int
    new_password: str
    pwd_confirm: str


class AuthTokenVerficicacaoSolic(SCBaseModel):
    username: str
    phone: Optional[str]
    email: Optional[str]


class AuthTokenVerficicacaoCreate(SCBaseModel):
    username: str
    enviar_por: Literal['WhatsApp', 'E-mail', 'SMS']
    phone: Optional[str]
    email: Optional[str]


class AuthTokenVerficicacaoResponse(SCBaseModel):
    msg: str


class AuthTokenValidacao(SCBaseModel):
    token: int
    username: str


class AuthTokenValidacaoResponse(SCBaseModel):
    uid: int
