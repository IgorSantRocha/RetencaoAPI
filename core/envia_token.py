from fastapi import HTTPException, status
from core.request import RequestEvolutionAPI
from schemas.auth_schema import AuthTokenVerficicacaoCreate, AuthTokenVerficicacaoResponse
from utils import format_whatsapp_number
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
        # Configurações do servidor
        smtp_host = 'smtp.hostinger.com'
        smtp_port = 587
        email_user = 'sys@c-trends.com.br'
        email_pass = 'Cr@$#2020'

        # Configuração do email
        de = 'sys@c-trends.com.br'
        para = self.email
        assunto = 'Token de alteração de senha'
        corpo = f"""
        <html>
        <head></head>
        <body>
            <h1>Olá!</h1>
            <p>Anote o token de alteração de senha: <b style="color: blue;">{token}</b>!</p>
        </body>
        </html>
        """

        # Criando a mensagem
        msg = MIMEMultipart()
        msg['From'] = de
        msg['To'] = para
        msg['Subject'] = assunto

        # Adicionando o corpo do email
        msg.attach(MIMEText(corpo, 'html'))

        # Enviando o email
        try:
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(email_user, email_pass)
            texto = msg.as_string()
            server.sendmail(de, para, texto)
            server.quit()
            print("Email enviado com sucesso!")
        except Exception as e:
            print(f"Falha ao enviar o email: {e}")

    async def _sms(self, token: int):
        pass
