from datetime import datetime
import xmlrpc.client
from fastapi import HTTPException, status
from core.config import settings
from schemas.auth_schema import AuthResponse, AuthCreate, AuthResetPassword, AuthTokenVerficicacaoCreate
from schemas.auth_schema import AuthTokenVerficicacaoResponse, AuthTokenValidacaoResponse, AuthTokenValidacao
from utils import valida_pwd, valida_username, generate_token


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
            [['user_id', '=', uid]]], {'fields': ['user_id', 'name', 'mobile_phone', 'work_email', 'company_id']})

        consulta_user = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password, 'res.users', 'search_read', [
            [['id', '=', uid]]], {'fields': ['id', 'name', 'partner_id']})

        consulta_partner = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password, 'res.partner', 'search_read', [
            [['id', '=', consulta_user[0]['partner_id'][0]]]], {'fields': ['id', 'name', 'l10n_br_cnpj_cpf']})

        dict_contulta = consulta_employee[0]
        resposta = AuthResponse(
            uid=uid,
            username=usr,
            name=dict_contulta['name'],
            phone=dict_contulta['mobile_phone'],
            email=dict_contulta['work_email'],
            cod_base=dict_contulta['company_id'][1],
            documento=consulta_partner[0]['l10n_br_cnpj_cpf']
        )
        return resposta

    async def cria_usuario(self, new_usr: AuthCreate) -> AuthResponse:

        if new_usr.pwd != new_usr.pwd_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="As senhas informadas não conferem!"
            )

        valida_pwd(new_usr.pwd)
        valida_username(new_usr.username)

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

        models.execute_kw(
            settings.odoo_db, uid_master, settings.odoo_password, 'hr.employee', 'create', [
                {
                    'name': new_usr.name,
                    'company_id': company[0]['id'],
                    'user_id': id_new,
                    'job_title': 'Técnico (courier)',
                    'mobile_phone': new_usr.phone,
                    'work_email': new_usr.email,
                    'employee_type': 'employee',
                    'marital': 'single'
                }])
        response = AuthResponse(
            uid=id_new,
            username=new_usr.username,
            name=new_usr.name,
            phone=new_usr.phone,
            email=new_usr.email,
            cod_base=new_usr.cod_base,
            documento=new_usr.documento
        )
        return response

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
