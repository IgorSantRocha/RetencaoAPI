import xmlrpc.client

odoo_url = "http://192.168.0.217:8069/"
odoo_db = "elotechsys"
odoo_username = 'fastapi'
odoo_password = 'Profeta#2'


common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_url))

uid = common.authenticate(odoo_db, odoo_username, odoo_password, {})

context = {'no_reset_password': True}

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_url))
consulta = models.execute_kw(odoo_db, uid, odoo_password, 'res.users', 'search_read', [
                             [['active', '=', True]]], {'fields': ['login', 'country_id', 'comment']})

id_new = models.execute_kw(
    odoo_db, uid, odoo_password, 'res.users', 'create', [
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
