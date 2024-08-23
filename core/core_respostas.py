from fastapi import HTTPException, status
from core.request import RequestEvolutionAPI
from schemas.auth_schema import AuthTokenVerficicacaoCreate, AuthTokenVerficicacaoResponse
from utils import format_whatsapp_number, format_sms_number
from core.config import settings
from core.email_smtp import EnvioEmailSmtp
from core.request import RequestClientUnipixAuth, RequestClientUnipixEnvio
from schemas.resposta_sms_schema import Sms


class Respostas():
    async def wpp(self, phone: str, msg: str, instancia: str):
        telefone_wpp = format_whatsapp_number(phone)
        client = RequestEvolutionAPI(
            instance=instancia,
            telefone=telefone_wpp,
            msg=msg
        )

        # manda a request ou erro 400
        response = await client.send_api_request()

        return response

    async def sms(self, sms_data: Sms):
        client_auth = RequestClientUnipixAuth()
        response_auth = await client_auth.send_api_request()
        access_token_auth = response_auth['access_token']

        headers = {'Authorization': f'Bearer {access_token_auth}'}

        telefone_envio = format_sms_number(sms_data.telefone)
        mensagem_resposta = f'Retorno da OS: {sms_data.os}\n{sms_data.conclusao}\n{sms_data.obs_atendente}'

        client_envio = RequestClientUnipixEnvio(
            headers=headers,
            telefone=telefone_envio,
            msg=mensagem_resposta,
            centroCustoId=293,  # Central de retenção
            produtoId=34,
            nome_envio=f'Retorno da OS 0800'
        )
        response_envio = await client_envio.send_api_request()

        return 'Mensagem enviada'
