from fastapi import HTTPException, status
from core.request import RequestEvolutionAPI
from schemas.auth_schema import AuthTokenVerficicacaoCreate, AuthTokenVerficicacaoResponse
from utils import format_whatsapp_number, format_sms_number
from core.config import settings
from core.email_smtp import EnvioEmailSmtp
from core.request import RequestClientUnipixAuth, RequestClientUnipixEnvio


class EnviaToken(AuthTokenVerficicacaoCreate):
    async def envia_token(self, token: int):
        if self.enviar_por == 'WhatsApp':
            resposta = await self._wpp(token)
        elif self.enviar_por == 'E-mail':
            resposta = await self._email(token)
        elif self.enviar_por == 'SMS':
            resposta = await self._sms(token)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'O método de envio escolhido não é uma opção válida!'
            )

        return resposta

    async def _wpp(self, token: int):
        telefone_wpp = format_whatsapp_number(self.phone)
        client = RequestEvolutionAPI(
            instance='chatbot-receptivo',
            telefone=telefone_wpp,
            msg=f'Olá, segue o token de alteração de senha.\nUsuário: *{self.username}*\nToken: *{token}*\n\n*Este Token expira em 5 minutos*'
        )

        # manda a request ou erro 400
        response = await client.send_api_request()

        return response

    async def _email(self, token: int):

        para = self.email
        assunto = 'Token de alteração - Central Retenção'
        corpo = f"""
        <html>
        <head></head>
        <body>
            <h1>Olá!</h1>
            <p>Anote o token de alteração de senha: <b style="color: blue;">{token}</b>!</p>
        </body>
        </html>
        """
        client = EnvioEmailSmtp(para, assunto, corpo)

        response = await client.envia_email()
        return response

    async def _sms(self, token: int):
        client_auth = RequestClientUnipixAuth()
        response_auth = await client_auth.send_api_request()
        access_token_auth = response_auth['access_token']

        headers = {'Authorization': f'Bearer {access_token_auth}'}

        telefone_envio = format_sms_number(self.phone)

        client_envio = RequestClientUnipixEnvio(headers, telefone_envio, token)
        response_envio = await client_envio.send_api_request()

        return response_envio
