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


class KeySC(SCBaseModel):
    remoteJid: str
    fromMe: bool
    id: str


class ExtendedTextMessageSC(SCBaseModel):
    text: str


class MessageSC(SCBaseModel):
    extendedTextMessage: ExtendedTextMessageSC


class ResponseEvolutionSC(SCBaseModel):
    key: KeySC
    message: MessageSC
    messageTimestamp: str
    status: str
