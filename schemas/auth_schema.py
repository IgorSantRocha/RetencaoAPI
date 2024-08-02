from pydantic import BaseModel as SCBaseModel


class Auth(SCBaseModel):
    username: str
    password: str
