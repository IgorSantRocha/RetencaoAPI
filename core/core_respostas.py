import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from core.request import RequestEvolutionAPI
from utils import format_sms_number
from core.request import RequestClientUnipixAuth, RequestClientUnipixEnvio
from schemas.resposta_sms_schema import Sms
from schemas.resposta_evolution_schema import MessageSchema
from schemas.tb_projeto_fedex_historico_schema import TbProjetoFedexHistoricoUpdate
from schemas.tb_projeto_fedex_schema import TbProjetoFedexUpdateCallidSC
from crud.crud_tb_projeto_fd_hist import tb_projeto_fd_hist
from crud.crud_tb_operacional import tb_fedex_operacional
from crud.crud_tb_projeto_fd import tb_projeto_fd_callid


class RespostaSMS():
    async def enviar(self, sms_data: Sms):
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


class RespostaWPP:

    def _monta_txt_resposta(self, os: str, atendente: str, conclusao: str, obs: str, protocolo_aut: bool, protocolo: str):
        '''Esta função faz apenas um concatenar das variáveis, montando o texto que será enviado no WPP'''
        enter = "\n"
        txt_retorno = f"*Retorno da OS:* {os}{enter}{enter}*Atendente:* {atendente}{enter}*Observações:*{enter}{conclusao}{enter}{obs}"
        if protocolo_aut:
            txt_retorno = f'{txt_retorno}{enter}{enter}*Anote o protocolo:* {protocolo}'
        return txt_retorno

    async def enviar(self, info_messagem: MessageSchema, db: AsyncSession):
        '''Chama as funções necessárias para obter as informações e envia a requisição para o EvolutionAPI'''

        info_callid = tb_projeto_fd_hist.get_last_by_filters(
            db=db,
            filters={'callid': {'operator': '==', 'value': info_messagem.callid}})

        if not info_callid:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Callid não encontrado')
        if info_callid.ip == 'Resposta enviada':
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Resposta já enviada!')

        tb_op = tb_fedex_operacional.get_last_by_filters(
            db=db,
            filters={'codigo': {'operator': '==', 'value': info_messagem.codigo_conclusao}})

        txt = self._monta_txt_resposta(
            os=info_messagem.os,
            atendente=info_messagem.atendente,
            conclusao=tb_op.conclusao_operador,
            obs=info_messagem.obs,
            protocolo_aut=tb_op.protocolo,
            protocolo=info_messagem.protocolo
        )

        # Monto o corpo da requisição
        client = RequestEvolutionAPI(
            instance='chatbot-receptivo',
            telefone=info_messagem.telefone,
            msg=txt
        )

        # manda a request ou erro 400
        try:
            response = await client.send_api_request()
        except httpx.HTTPStatusError as exc:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        obj_hist_in = TbProjetoFedexHistoricoUpdate(
            os=info_callid.os,
            ip='Resposta enviada'
        )
        tb_projeto_fd_hist.update(
            db=db,
            db_obj=info_callid,
            obj_in=obj_hist_in
        )

        obj_tb_projeto_fd = tb_projeto_fd_callid.get_last_by_filters(
            db=db,
            filters={'call_id': {'operator': '==', 'value': info_messagem.callid}})

        if not obj_tb_projeto_fd:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Callid não encontrado')

        obj_in_tb_projeto_fd = TbProjetoFedexUpdateCallidSC(
            call_id=None
        )

        tb_projeto_fd_callid.update(
            db=db,
            db_obj=obj_tb_projeto_fd,
            obj_in=obj_in_tb_projeto_fd
        )

        return response
