from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.tb_projeto_fedex_historico_schema import TbProjetoFedexHistoricoCreateSC, TbProjetoFedexHistoricoSC
from schemas.tb_projeto_fedex_schema import TbProjetoFedexBaseSC, TbProjetoFedexCreateSC
from crud.crud_lista_projeto import lista_projetos
from crud.crud_tb_projeto_fd import tb_projeto_fd
from crud.crud_tb_projeto_fd_hist import tb_projeto_fd_hist
from core.config import settings
import uuid
import logging

logger = logging.getLogger(__name__)


class Abertura():
    async def abertura_os(self, info_os: TbProjetoFedexHistoricoSC, meio_captura: str, db: AsyncSession) -> TbProjetoFedexCreateSC:
        chave: str = await self._gerar_id_unico()
        # for os in info_os.oss:
        #    chave += os

        # if len(chave) > 250:
        #    chave = chave[:250]

        # Regra para colocar uma informação no final da OBS para o caso de a abertura ter mais de uma OS
        obs_oss_agregadas = ''
        if len(info_os.oss) > 1:
            qtd_oss: int = len(info_os.oss)-1
            # obs_oss_agregadas = f'\n\n ! ATENÇÃO !\nOS agregada a outra(s) {qtd_oss}.\nOs principal: {info_os.oss[0]}'
            obs_oss_agregadas = f'\n\n ! ATENÇÃO ! OS agregada a outra(s) {qtd_oss}. Os principal: {info_os.oss[0]}'

        for os in info_os.oss:
            # Crio o objeto com os campos padrões
            obj_abertura = await self.cria_obj_in(info_os, db, meio_captura, os)
            obj_abertura.chave = chave
            if meio_captura != 'SYS':
                obj_abertura.atendente_abertura = meio_captura
            # faço uma consulta para saber se a OS já existe e decidir entre update ou insert
            consulta_os: TbProjetoFedexBaseSC = tb_projeto_fd.get_first_by_filter(
                db=db, filterby='os', filter=obj_abertura.os)

            if consulta_os:
                logger.info("Criando modelo para update")
                dt_abertura_antiga: datetime = consulta_os.dt_abertura
                data_atual: datetime = datetime.now()
                if dt_abertura_antiga.date() == data_atual.date():
                    obj_abertura.reabertura = 'S'

                novo_hist = consulta_os.problema_apresentado + \
                    f'\n' + obj_abertura.problema_apresentado+obs_oss_agregadas
                obj_abertura.problema_apresentado = novo_hist

                obj_abertura.cliente = consulta_os.cliente or '...'
                obj_abertura.subprojeto = consulta_os.subprojeto or '...'

                logger.info("Realizando o update")
                tb_projeto_fd.update(
                    db=db, db_obj=consulta_os, obj_in=obj_abertura)
            else:
                obj_abertura.problema_apresentado += obs_oss_agregadas
                logger.info("Realizando o create")
                tb_projeto_fd.create(db=db, obj_in=obj_abertura)

            logger.info("Inserindo informação na tabela de histórico")
            obj_in_hist = TbProjetoFedexHistoricoCreateSC(
                os=obj_abertura.os,
                problema_apresentado=obj_abertura.problema_apresentado,
                tecnico=obj_abertura.nome_tecnico,
                callid=obj_abertura.call_id
            )
            tb_projeto_fd_hist.create(db=db, obj_in=obj_in_hist)

        return obj_abertura

    async def _gerar_id_unico(self) -> str:
        logger.info("Gerando ID único para o callid")
        # Obter a data/hora atual
        data_hora_atual = datetime.now().strftime('%d%m%y%H%M%S')

        # Gerar um UUID aleatório
        # Remover os hífens para garantir que seja uma string
        uuid_aleatorio = str(uuid.uuid4()).replace('-', '')

        # Combinar a data/hora atual e o UUID
        id_unico = data_hora_atual + "$" + uuid_aleatorio

        return id_unico

    async def cria_obj_in(self, info_os: TbProjetoFedexHistoricoSC, db: AsyncSession, meio_captura: str, os: str) -> TbProjetoFedexCreateSC:
        '''
        Defino os valores padrões das variáveis, criando um objeto com os valores necessários para abrir o caso na fila
        '''
        logger.info("Criando obj")
        info_os.projeto = info_os.projeto.upper()

        if info_os.projeto != 'CIELO' and os.startswith('CLC'):
            info_os.projeto = 'CIELO'
        elif info_os.projeto == 'CIELO' and not os.startswith('CLC'):
            info_os.projeto = 'CTBPO'
        elif info_os.projeto == 'FISERV':
            info_os.projeto = 'FIRST'

        if meio_captura == 'CHAT':
            call_id = await self._gerar_id_unico()
        else:
            call_id = None

        data_hora_atual = datetime.now()
        data_hora_formatada = data_hora_atual.strftime("%d/%m/%Y %H:%M:%S")
        data_hora_formato_sql_server: str = data_hora_atual.strftime(
            "%Y-%m-%d %H:%M:%S.%f")[:-3]
        obj_in = TbProjetoFedexCreateSC(
            os=os,
            chave=os,
            dt_abertura=data_hora_formato_sql_server,
            dt_fechamento=data_hora_formato_sql_server,
            problema_apresentado=f'|{data_hora_formatada} - Técnico: {info_os.tecnico} - Ocorrência: {info_os.ocorrencia}  - {info_os.problema_apresentado}',
            ocorrencia=info_os.ocorrencia,
            projeto=info_os.projeto,
            tipo_atendimento=info_os.tipo_atendimento,

            atendente_abertura=info_os.tecnico,
            retorno_tecnico='Sim' if info_os.ocorrencia in (
                'Técnico em rota', 'Coleta realizada c/ sucesso', 'Insucesso na visita', 'Entrega realizada') else 'Não',
            nome_tecnico=info_os.tecnico,
            telefone_tecnico=info_os.telefone_tecnico,
            acao_D29='...',
            versao=settings.API_VERSION,

            fase='D+0',
            etapa='D+0',
            tipo='',
            acao_d1='...',
            cliente='...',
            subprojeto='...',
            status='...',
            conclusao_operador='',
            definicao='',
            status_relatorio='',
            call_id=call_id,
            reabertura=None,
            uid=info_os.uid,
            latitude=info_os.latitude,
            longitude=info_os.longitude,
            imageurl=info_os.imageurl,
            unidade=info_os.unidade
        )

        # STATUS
        if info_os.ocorrencia == 'Técnico em rota':
            obj_in.status = 'SEGUIR ROTA - MENSAGEM ENVIADA'
        elif info_os.ocorrencia in ('Coleta realizada c/ sucesso', 'Entrega realizada'):
            obj_in.status = 'PEDIDO REALIZADO'

        # CONCLUSAO
        if info_os.ocorrencia == 'Técnico em rota':
            obj_in.conclusao_operador = 'Enviada mensagem no WhatsApp'
        elif info_os.ocorrencia == 'Coleta realizada c/ sucesso':
            obj_in.conclusao_operador = 'Informação de coleta recebida. Técnico autorizado a seguir rota.'
        elif info_os.ocorrencia == 'Entrega realizada':
            obj_in.conclusao_operador = 'Informação recebida. Seguir viagem'

        # Definicao
        if info_os.ocorrencia == 'Técnico em rota':
            obj_in.definicao = 'PENDENTE / EM ROTA'
        elif info_os.ocorrencia in ('Coleta realizada c/ sucesso', 'Entrega realizada'):
            obj_in.definicao = 'PEDIDO REALIZADO'

        # status relatorio
        if info_os.ocorrencia == 'Técnico em rota':
            obj_in.status_relatorio = 'PENDENTE / EM ROTA'
        elif info_os.ocorrencia in ('Coleta realizada c/ sucesso', 'Entrega realizada'):
            obj_in.status_relatorio = 'SEM TRATATIVA DA CENTRAL'

        consulta_cliente = lista_projetos.get_multi_filter(
            db=db, filterby='projeto', filter=info_os.projeto)
        if consulta_cliente:
            obj_in.cliente = consulta_cliente[0].cliente

        return obj_in
