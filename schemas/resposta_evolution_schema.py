from pydantic import BaseModel as SCBaseModel


class MessageSchema(SCBaseModel):
    callid: str
    telefone: str
    os: str
    protocolo: str
    atendente: str
    codigo_conclusao: str
    obs: str

    class Config:
        from_attributes = True


'''
Criando modelo de resposta do Evolution API
'''


class Key(SCBaseModel):
    remoteJid: str
    fromMe: bool
    id: str


class ExtendedTextMessage(SCBaseModel):
    text: str


class Message(SCBaseModel):
    extendedTextMessage: ExtendedTextMessage


class ResponseEvolution(SCBaseModel):
    key: Key
    message: Message
    messageTimestamp: str
    status: str
