import logging
import httpx
from opentelemetry.propagate import inject
from core.config import settings
from datetime import datetime
logger = logging.getLogger()


async def log_request_result(prefix, endpoint, method, request_data, res):
    logger.info(
        f"{prefix} | request_method: {method} | request_url: {endpoint!r} | request_body: {request_data} | response_code: {res.status_code} | response_body {res.text}"
    )


class RequestEvolutionAPI:
    def __init__(self,  instance: str, telefone: str, msg: str, timeout: int = 100) -> None:
        self.method = 'POST'
        self.url = 'http://192.168.0.213:3000/message/sendText/' + instance
        self.request_data = {
            "number": telefone,
            "options": {
                "delay": 1200,
                "presence": "composing",
                "linkPreview": "false"
            },
            "textMessage": {
                "text": msg
            }
        }
        self.headers = {
            'apikey': 'rJ9aWxBaX82Pn7vC15tlL5ZBoCwCTLtnvj73OxsycfcI1o84vv9Y2Hh2I2jFNKx9iQVUqteUOk4pWI7g'}
        self.timeout = timeout
        inject(carrier=self.headers)

    async def send_api_request(self):
        logger.info(f"Sending a {self.method} request to: {self.url}")
        logger.info(f"Request body/params: {self.request_data}")
        logger.info(f"Request HEADERS: {self.headers}")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                request = httpx.Request(self.method.upper(), url=self.url,
                                        **{f"{'params' if self.method == 'get' else 'json'}": self.request_data},
                                        headers=self.headers)
                response = await client.send(request)
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                await log_request_result('request_error', self.url, self.method, self.request_data, response)
                raise exc

            await log_request_result('request_success', self.url, self.method, self.request_data, response)
            return response.json()


class RequestClientUnipixAuth:
    def __init__(self, timeout: int = 100) -> None:
        self.method = 'POST'
        self.url = settings.unipix_url_auth
        self.request_data = {
            "email": settings.unipix_username,
            "password": settings.unipix_password
        }
        self.headers = {}
        self.timeout = timeout
        inject(carrier=self.headers)

    async def send_api_request(self):
        logger.info(f"Sending a {self.method} request to: {self.url}")
        logger.info(f"Request body/params: {self.request_data}")
        logger.info(f"Request HEADERS: {self.headers}")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                request = httpx.Request(self.method.upper(), url=self.url,
                                        **{f"{'params' if self.method == 'get' else 'json'}": self.request_data},
                                        headers=self.headers)
                response = await client.send(request)
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                await log_request_result('request_error', self.url, self.method, self.request_data, response)
                raise exc

            await log_request_result('request_success', self.url, self.method, self.request_data, response)
            return response.json()


class RequestClientUnipixEnvio:
    def __init__(self, headers, telefone: str, tokenVerif: str, timeout: int = 100) -> None:
        self.method = 'POST'
        self.url = settings.unipix_url_envio
        self.request_data = {
            "agendamentos": [
                {
                    "data": datetime.now(),
                    "quantidade": 1
                }
            ],
            "centroCustoId": 292,
            "envios": [
                {
                    "mensagemNumero": "Código de verificação CENTRAL RETENCAO",
                    "numero": telefone,
                    "smsClienteId": "string"
                }
            ],
            "mensagemCampanha": f"Código de verificação CENTRAL RETENCAO: {tokenVerif}",
            "nome": "CTB - Código de verificação",
            "produtoId": 34,
            "telefones": telefone,
            "urlCallbackEntrega": "string",
            "urlCallbackResposta": "string",
            "gerarUrlEncurtada": False
        }
        self.headers = headers
        self.timeout = timeout
        inject(carrier=self.headers)


class TemplateRequestClient:
    def __init__(self, method, url: str, headers, request_data: dict = None, timeout: int = 100) -> None:
        self.method = method
        self.url = url
        self.request_data = request_data
        self.headers = headers
        self.timeout = timeout
        inject(carrier=self.headers)

    async def send_api_request(self):
        logger.info(f"Sending a {self.method} request to: {self.url}")
        logger.info(f"Request body/params: {self.request_data}")
        logger.info(f"Request HEADERS: {self.headers}")

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                request = httpx.Request(self.method.upper(), url=self.url,
                                        **{f"{'params' if self.method == 'get' else 'json'}": self.request_data},
                                        headers=self.headers)
                response = await client.send(request)
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                await log_request_result('request_error', self.url, self.method, self.request_data, response)
                raise exc

            await log_request_result('request_success', self.url, self.method, self.request_data, response)
            return response.json()
