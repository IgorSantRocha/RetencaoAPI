import xmlrpc.client
from core.config import settings

common = xmlrpc.client.ServerProxy(
    '{}/xmlrpc/2/common'.format(settings.odoo_url))

uid = common.authenticate(
    settings.odoo_db, settings.odoo_username, settings.odoo_password, {})

context = {'no_reset_password': True}

models = xmlrpc.client.ServerProxy(
    '{}/xmlrpc/2/object'.format(settings.odoo_url))
consulta = models.execute_kw(settings.odoo_db, uid, settings.odoo_password, 'res.users', 'search_read', [
                             [['active', '=', True]]], {'fields': ['login', 'country_id', 'comment']})

id_new = models.execute_kw(
    settings.odoo_db, uid, settings.odoo_password, 'res.users', 'create', [
        {
            'name': "Teste",
            'login': 'Teste',
            'company_ids': [1],
            'company_id': 1,
            'password': '123456',
            'sel_groups_1_10_11': 10,
            'lang': 'pt_BR'
        }], {'context': context})

print(consulta)
print(id_new)
