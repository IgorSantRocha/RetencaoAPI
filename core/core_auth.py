import xmlrpc.client
import re
from fastapi import HTTPException, status
from core.config import settings
from schemas.auth_schema import AuthResponse, AuthCreate


class AuthOdoo:
    async def autentica_usuario(self, usr: str, pwd: str) -> AuthResponse:
        # primeiro tento autenticar o usuário com as credenciais passadas
        uid = await self._auth_odoo(usr=usr, pwd=pwd)

        '''logo com usuário adm para poder consultar a tabela de funcionários 
        e retornar as informações de cadastro do usuário
        '''
        uid_master = await self._auth_odoo(settings.odoo_username, settings.odoo_password)

        models = self._cria_object()

        consulta = models.execute_kw(settings.odoo_db, uid_master, settings.odoo_password, 'hr.employee', 'search_read', [
            [['user_id', '=', uid]]], {'fields': ['user_id', 'name', 'mobile_phone', 'work_email', 'company_id']})

        dict_contulta = consulta[0]
        resposta = AuthResponse(
            uid=uid,
            username=usr,
            name=dict_contulta['name'],
            phone=dict_contulta['mobile_phone'],
            email=dict_contulta['work_email'],
            cod_base=dict_contulta['company_id'][1]
        )
        return resposta

    async def cria_usuario(self, new_usr: AuthCreate) -> AuthResponse:

        if new_usr.pwd != new_usr.pwd_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="As senhas informadas não conferem!"
            )

        await self._valida_pwd(new_usr.pwd)

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
            cod_base=new_usr.cod_base
        )
        return response

    async def _valida_pwd(self, pwd):
       # Verifica o comprimento da senha
        if len(pwd) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve conter pelo menos 6 caracteres!"
            )

        # Verifica se contém pelo menos uma letra maiúscula
        if not re.search(r'[A-Z]', pwd):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve conter pelo menos uma letra maiúscula!"
            )

        # Verifica se contém pelo menos uma letra minúscula
        if not re.search(r'[a-z]', pwd):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve conter pelo menos uma letra minúscula!"
            )

        # Verifica se contém pelo menos um número
        if not re.search(r'[0-9]', pwd):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve conter pelo menos um número!"
            )

        # Verifica se contém pelo menos um caractere especial
        if not re.search(r'[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};:\'",<>\./?]', pwd):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve conter pelo menos um caractere especial!"
            )

        return True

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
