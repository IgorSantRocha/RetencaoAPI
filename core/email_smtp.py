from core.config import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EnvioEmailSmtp:
    def __init__(self,   para: str, assunto: str, corpo: str) -> None:
        # Configurações do servidor
        self.smtp_host = settings.email_smtp_host
        self.smtp_port = settings.email_smtp_port
        self.email_user = settings.email_user
        self.email_pass = settings.email_pass
        self.de = settings.email_user
        self.para = para
        self.assunto = assunto
        self.corpo = corpo

    async def envia_email(self):
        # Criando a mensagem
        msg = MIMEMultipart()
        msg['From'] = self.de
        msg['To'] = self.para
        msg['Subject'] = self.assunto

        # Adicionando o corpo do email
        msg.attach(MIMEText(self.corpo, 'html'))

        # Enviando o email
        try:
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            texto = msg.as_string()
            server.sendmail(self.de, self.para, texto)
            server.quit()
            return "Email enviado com sucesso!"
        except Exception as e:
            return f"Falha ao enviar o email: {e}"
