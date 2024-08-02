import xmlrpc.client
import re
from fastapi import HTTPException, status
from core.config import settings


class AuthOdoo:
    async def autentica_usuario(self, usr: str, pwd: str) -> int:
        common = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(settings.odoo_url))
        uid = common.authenticate(
            settings.odoo_db, usr, pwd, {})

        if not uid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos!"
            )

        return uid

    async def cria_usuario(self,
                           usr: str,
                           pwd: str,
                           pwd_confirm: str,
                           name: str,
                           cod_rep: str,
                           phone: str,
                           email: str):

        if pwd != pwd_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="As senhas informadas não conferem!"
            )

        self._valida_pwd(pwd)

        common = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(settings.odoo_url))

        uid = common.authenticate(
            settings.odoo_db, settings.odoo_username, settings.odoo_password, {})

        models = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/object'.format(settings.odoo_url))

        company = models.execute_kw(settings.odoo_db, uid, settings.odoo_password, 'res.company', 'search_read', [
            [['name', '=', cod_rep]]], {'fields': ['id', 'name']})

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Não foi possível encontrar nenhum REP = {cod_rep}"
            )

        context = {'no_reset_password': True}
        id_new = models.execute_kw(
            settings.odoo_db, uid, settings.odoo_password, 'res.users', 'create', [
                {
                    'name': name,
                    'login': usr,
                    'company_ids': [company[0]['id']],
                    'company_id': company[0]['id'],
                    'password': pwd,
                    'sel_groups_1_10_11': 10,
                    'lang': 'pt_BR'
                }], {'context': context})

        models.execute_kw(
            settings.odoo_db, uid, settings.odoo_password, 'hr.employee', 'create', [
                {
                    'name': name,
                    'company_id': company[0]['id'],
                    'user_id': id_new,
                    'job_title': 'Técnico (courier)',
                    'mobile_phone': phone,
                    'work_email': email,
                    'employee_type': 'employee',
                    'marital': 'single'
                }])

        return id_new

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
