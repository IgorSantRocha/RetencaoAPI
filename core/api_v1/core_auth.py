from datetime import datetime
import xmlrpc.client
from fastapi import HTTPException, status
from core.config import settings
from schemas.api_v1.auth_schema import AuthResponse, AuthCreate, AuthResetPassword, AuthTokenVerficicacaoCreate, AuthAlterCadUser
from schemas.api_v1.auth_schema import AuthTokenVerficicacaoResponse, AuthTokenValidacaoResponse, AuthTokenValidacao, AuthTokenVerficicacaoSolic
from schemas.api_v1.usr_schema import UserGeralSC
from schemas.api_v1.tb_retencaoapi_tokens_schema import APITokensCreateSC, APITokensUpdateSC
from utils import valida_pwd, valida_username, generate_token, valida_cpf, valida_email
from core.api_v1.envia_token import EnviaToken
from sqlalchemy.ext.asyncio import AsyncSession
from crud.api_v1.crud_users import user_211, user_212
from crud.api_v1.crud_tb_retencaoapi_tokens import tb_api_tokens


class Auth2Factores:
    async def verifica_credenciais(self, usr: str, pwd: str, db_211: AsyncSession):
        usuario_211 = user_211.get_last_by_filters(
            db_211,
            filters={'usr': {'operator': '==', 'value': usr},
                     'pwd': {'operator': '==', 'value': pwd}})
        # usuario_212 = user_212.get_last_by_filters(db_212,filters={'usr': {'operator': '==', 'value': usr},'pwd': {'operator': '==', 'value': pwd}})

        if not usuario_211:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Usuário ou senha inválidos')

        if usuario_211:
            if not usuario_211.email:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Usuário não tem e-mail cadastrado. Envie uma solicitação para que o e-mail seja adicionado')

        token = APITokensCreateSC(
            usr=usuario_211.usr,
            token=generate_token()
        )
        token_gerado = tb_api_tokens.create(db=db_211, obj_in=token)
        envio_token = EnviaToken(
            email=usuario_211.email,
            phone='',
            username=usuario_211.usr,
            enviar_por='E-mail'
        )

        envio = await envio_token.envia_token(
            token=token.token,
            assunto='C-Trends - Token de verificação',
            texto='Segue token de verificação para login no sistema')

        return token_gerado.id

    async def valida_token(self, usr: str, token: str, db_211: AsyncSession):

        dados_token = tb_api_tokens.get_last_by_filters(
            db_211,
            filters={'usr': {'operator': '==', 'value': usr},
                     'token':{'operator': '==', 'value': token},
                     'expiraem': {'operator': '>=', 'value': datetime.now()},
                     'usado': {'operator': '==', 'value': False}})

        if not dados_token:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Token inválido')

        dados_token_usado = APITokensUpdateSC(
            id=dados_token.id,
            usado=True
        )

        tb_api_tokens.update(
            db=db_211,
            db_obj=dados_token,
            obj_in=dados_token_usado)

        usuario_211 = user_211.get_last_by_filters(
            db_211,
            filters={'usr': {'operator': '==', 'value': usr}})
        # usuario_212 = user_212.get_last_by_filters(db_212,filters={'usr': {'operator': '==', 'value': usr}})

        retorno_usr = UserGeralSC(
            id=usuario_211.id,
            usr=usuario_211.usr,
            nome=usuario_211.nome,
            nivel=usuario_211.nivel,
            niveldescricao=usuario_211.niveldescricao
        )

        return retorno_usr


class AuthOdoo:
    async def autentica_usuario(self, usr: str, pwd: str) -> AuthResponse:
        # primeiro tento autenticar o usuário com as credenciais passadas
        uid = await self._auth_odoo(usr=usr, pwd=pwd)

        '''logo com usuário adm para poder consultar a tabela de funcionários 
        e retornar as informações de cadastro do usuário
        '''
        uid_master = await self._auth_odoo(settings.odoo_username, settings.odoo_password)

        models = self._cria_object()

        consulta_employee = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password, 'hr.employee', 'search_read', [
            [['user_id', '=', uid]]], {'fields': ['user_id', 'name', 'mobile_phone', 'work_email', 'company_id', 'job_title']})

        consulta_user = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password, 'res.users', 'search_read', [
            [['id', '=', uid]]], {'fields': ['id', 'name', 'partner_id']})

        consulta_partner = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password, 'res.partner', 'search_read', [
            [['id', '=', consulta_user[0]['partner_id'][0]]]], {'fields': ['id', 'name', 'l10n_br_cnpj_cpf']})

        dict_contulta = consulta_employee[0]
        resposta = AuthResponse(
            uid=uid,
            username=usr,
            name=dict_contulta['name'],
            phone=dict_contulta['mobile_phone'] if dict_contulta['mobile_phone'] else '',
            email=dict_contulta['work_email'],
            cod_base=dict_contulta['company_id'][1],
            documento=consulta_partner[0]['l10n_br_cnpj_cpf'] if consulta_partner[0]['l10n_br_cnpj_cpf'] else '',
            nome_unidade=dict_contulta['job_title']
        )
        return resposta

    async def cria_usuario(self, new_usr: AuthCreate) -> AuthResponse:
        valida_username(new_usr.username)
        valida_email(new_usr.email)
        valida_cpf(new_usr.documento)
        valida_pwd(pwd=new_usr.pwd)
        if new_usr.pwd != new_usr.pwd_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="As senhas informadas não conferem!"
            )

        uid_master = await self._auth_odoo(settings.odoo_username, settings.odoo_password)

        models = self._cria_object()

        # Consulto o id e o nome da base de acordo com o cod_rep informado.
        # Para poder vincular o usuário do técnico à base
        company = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password, 'res.company', 'search_read', [
            [['name', '=', new_usr.cod_base]]], {'fields': ['id', 'name']})

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possível encontrar nenhum REP = {new_usr.cod_rep}"
            )

        context = {'no_reset_password': True}
        try:
            id_new = models.execute_kw(
                settings.odoo_db, uid_master, settings.odoo_password, 'res.users', 'create', [
                    {
                        'name': new_usr.name,
                        'login': new_usr.username,
                        'company_ids': [company[0]['id']],
                        'company_id': company[0]['id'],
                        'password': new_usr.pwd,
                        'l10n_br_cnpj_cpf': new_usr.documento,
                        'sel_groups_1_10_11': 10,
                        'lang': 'pt_BR'
                    }], {'context': context})
        except xmlrpc.client.Fault as fer:
            if fer.faultString == 'The operation cannot be completed: Este CPF/CNPJ já está em uso por outro parceiro!':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail='Este CPF/CNPJ já está em uso por outro parceiro!')

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=fer.faultString)

        models.execute_kw(
            settings.odoo_db, uid_master, settings.odoo_password, 'hr.employee', 'create', [
                {
                    'name': new_usr.name,
                    'company_id': company[0]['id'],
                    'user_id': id_new,
                    'job_title': new_usr.nome_unidade,
                    'mobile_phone': new_usr.phone,
                    'work_email': new_usr.email,
                    'employee_type': 'freelance',
                    'marital': 'single'
                }])

        response = AuthResponse(
            uid=id_new,
            username=new_usr.username,
            name=new_usr.name,
            phone=new_usr.phone,
            email=new_usr.email,
            cod_base=new_usr.cod_base,
            documento=new_usr.documento,
            nome_unidade=new_usr.nome_unidade
        )
        return response

    async def deleta_usuario(self, usr: str, pwd: str) -> int:
        # primeiro tento autenticar o usuário com as credenciais passadas
        uid = await self._auth_odoo(usr=usr, pwd=pwd)

        '''logo com usuário adm para poder consultar a tabela de funcionários 
        e retornar as informações de cadastro do usuário
        '''
        uid_master = await self._auth_odoo(settings.odoo_username, settings.odoo_password)

        models = self._cria_object()

        consulta_employee = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password, 'hr.employee', 'search_read', [
            [['user_id', '=', uid]]], {'fields': ['user_id', 'id', 'mobile_phone', 'work_email', 'company_id']})

        consulta_user = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password, 'res.users', 'search_read', [
            [['id', '=', uid]]], {'fields': ['id', 'name', 'partner_id']})

        consulta_partner = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password, 'res.partner', 'search_read', [
            [['id', '=', consulta_user[0]['partner_id'][0]]]], {'fields': ['id', 'name', 'l10n_br_cnpj_cpf']})

        models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password,
                          'res.users', 'unlink', [[consulta_user[0]['id']]])
        models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password,
                          'res.partner', 'unlink', [[consulta_partner[0]['id']]])
        models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password,
                          'hr.employee', 'unlink', [[consulta_employee[0]['id']]])

        return uid

    async def busca_info_verificacao(self, username: str):
        uid_master = await self._auth_odoo(settings.odoo_username, settings.odoo_password)

        models = self._cria_object()
        uids = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password,
                                 'res.users', 'search_read', [
                                     [['login', '=', username]]], {'fields': ['id']})

        if not uids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Username não encontrado!"
            )
        uid = uids[0]['id']

        consulta_employee = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password, 'hr.employee', 'search_read', [
            [['user_id', '=', uid]]], {'fields': ['user_id', 'name', 'mobile_phone', 'work_email', 'company_id']})

        dict_contulta = consulta_employee[0]
        response = AuthTokenVerficicacaoSolic(
            username=username,
            phone=dict_contulta['mobile_phone'],
            email=dict_contulta['work_email']
        )
        return response

    async def cria_token_verificacao(self, auth_data: AuthTokenVerficicacaoCreate):
        uid_master = await self._auth_odoo(settings.odoo_username, settings.odoo_password)
        models = self._cria_object()
        uids = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password,
                                 'res.users', 'search_read', [
                                     [['login', '=', auth_data.username]]], {'fields': ['id']})

        if not uids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Username não encontrado!"
            )
        uid = uids[0]['id']

        token = generate_token()
        consulta = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password,
                                     'user.token.alter.pwd',
                                     'create', [
                                         {
                                             'token': token,
                                             'res_users_id': uid,
                                             'token_usado': False
                                         }])
        envio_token = EnviaToken(
            email=auth_data.email,
            phone=auth_data.phone,
            username=auth_data.username,
            enviar_por=auth_data.enviar_por
        )

        envio = await envio_token.envia_token(token=token)

        resp = AuthTokenVerficicacaoResponse(
            msg=f'Token gerado e enviado por {auth_data.enviar_por}')

        return resp

    async def valida_token_verificacao(self, auth_data: AuthTokenValidacao):
        uid_master = await self._auth_odoo(settings.odoo_username, settings.odoo_password)
        models = self._cria_object()
        consulta = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password,
                                     'user.token.alter.pwd', 'search_read', [
                                         [['token', '=', auth_data.token],
                                          ['token_usado', '=', False],
                                          ['expira_em', '>=', datetime.now()]
                                          ]],
                                     {'fields': ['id', 'res_users_id', 'token_usado', 'expira_em']})

        if not consulta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Token não encontrado!"
            )

        uid_por_username = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password,
                                             'res.users', 'search_read', [
                                                 [['login', '=', auth_data.username]]], {'fields': ['id']})

        uid_por_username = uid_por_username[0]['id']

        uid_token = AuthTokenValidacaoResponse(
            uid=consulta[0]['res_users_id'][0])

        # valido se o token enviado foi gerado para o mesmo usuário que solicitou a validação
        if uid_token.uid != uid_por_username:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Token inválido!"
            )

        # marco o token como usado.
        models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password,
                          'user.token.alter.pwd', 'write', [
                              [consulta[0]['id']], {'token_usado': True}])

        return uid_token

    async def altera_senha(self, reset_pwd: AuthResetPassword):
        valida_pwd(reset_pwd.new_password)
        if reset_pwd.new_password != reset_pwd.pwd_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="As senhas informadas não conferem!"
            )

        uid_master = await self._auth_odoo(settings.odoo_username, settings.odoo_password)

        models = self._cria_object()

        consulta = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password, 'res.users', 'write', [
            [reset_pwd.uid], {'password': reset_pwd.new_password}])

        return reset_pwd

    async def altera_cadastro(self, cad_data: AuthAlterCadUser):
        uid_master = await self._auth_odoo(settings.odoo_username, settings.odoo_password)

        models = self._cria_object()
        employee_ids = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password,
                                         'hr.employee', 'search_read', [
                                             [['user_id', '=', cad_data.uid]]], {'fields': ['id']})

        if not employee_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Username não encontrado!"
            )
        employee_id = employee_ids[0]['id']

        models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password, 'hr.employee', 'write', [
            [employee_id], {
                'name': cad_data.name,
                'work_email': cad_data.email,
                'mobile_phone': cad_data.phone
            }])
        return cad_data

    async def _auth_odoo(self, usr: str, pwd: str) -> int:
        common = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(settings.odoo_url))

        uid = common.authenticate(
            settings.odoo_db, usr, pwd, {})

        if not uid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos!"
            )
        return uid

    def _cria_object(self) -> xmlrpc.client.ServerProxy:
        models = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/object'.format(settings.odoo_url))

        return models
