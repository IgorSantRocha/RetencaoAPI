from pydantic import BaseModel as SCBaseModel, constr, Field, validator
from typing import Literal, Optional
import re


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
    nome_unidade: str
    documento: str


class AuthCreate(SCBaseModel):
    username: str = Field('Exemplo_01', min_length=6,
                          description="Deve ter no mínimo 6 caracteres e conter apenas letras, números e underline.")
    pwd: str = Field('Exemplo@1', min_length=6,
                     description="Deve ter no mínimo 6 caracteres e incluir letras maiúsculas, minúsculas, números e caracteres especiais.")
    pwd_confirm: str
    name: str
    phone: str
    email: str
    cod_base: str
    nome_unidade: str
    documento: str


class AuthResetPassword(SCBaseModel):
    uid: int
    new_password: str = Field('Exemplo@1', min_length=6,
                              description="Deve ter no mínimo 6 caracteres e incluir letras maiúsculas, minúsculas, números e caracteres especiais.")
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


class AuthAlterCadUser(SCBaseModel):
    uid: int
    name: str
    phone: str
    email: str
