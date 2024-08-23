import json
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
        self.url = settings.evolution_api_url + instance
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
            'apikey': settings.evolution_api_apikey}
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

            try:
                # Decodificando o conteúdo usando ISO-8859-1
                response_content = response.content.decode('iso-8859-1')
                return json.loads(response_content)
            except UnicodeDecodeError as e:
                logger.error(f"Failed to decode response: {str(e)}")
                raise
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON: {str(e)}")
                raise


class RequestClientUnipixEnvioToken:
    def __init__(self, headers, telefone: str, tokenVerif: str, timeout: int = 100) -> None:
        self.method = 'POST'
        self.url = settings.unipix_url_envio
        self.request_data = {
            "agendamentos": [
                {
                    "data": "2022-09-13T15:58:53.889Z",
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

    async def send_api_request(self):
        logger.info(f"**************iniciando segunda request *************")
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
            try:
                # Decodificando o conteúdo usando ISO-8859-1
                response_content = response.content.decode('iso-8859-1')
                return json.loads(response_content)
            except UnicodeDecodeError as e:
                logger.error(f"Failed to decode response: {str(e)}")
                raise
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON: {str(e)}")
                raise


class RequestClientUnipixEnvio:
    def __init__(self,
                 headers,
                 telefone: str,
                 msg: str,
                 centroCustoId: int,
                 produtoId: int,
                 nome_envio: str = 'Envio direto',
                 timeout: int = 100) -> None:
        self.method = 'POST'
        self.url = settings.unipix_url_envio
        self.request_data = {
            "agendamentos": [
                {
                    "data": "2022-09-13T15:58:53.889Z",
                    "quantidade": 1
                }
            ],
            "centroCustoId": centroCustoId,
            "envios": [
                {
                    "mensagemNumero": nome_envio,
                    "numero": telefone,
                    "smsClienteId": "string"
                }
            ],
            "mensagemCampanha": msg,
            "nome": nome_envio,
            "produtoId": produtoId,
            "telefones": telefone,
            "urlCallbackEntrega": "string",
            "urlCallbackResposta": "string",
            "gerarUrlEncurtada": False
        }
        self.headers = headers
        self.timeout = timeout
        inject(carrier=self.headers)

    async def send_api_request(self):
        logger.info(f"**************iniciando segunda request *************")
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
            try:
                # Decodificando o conteúdo usando ISO-8859-1
                response_content = response.content.decode('iso-8859-1')
                return json.loads(response_content)
            except UnicodeDecodeError as e:
                logger.error(f"Failed to decode response: {str(e)}")
                raise
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON: {str(e)}")
                raise


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
