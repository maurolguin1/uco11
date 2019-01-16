# -*- coding: utf-8 -*-
{
    'name': "Rate currency",

    'summary': """
        rate apply 20 digits""",

    'description': """
       rate apply 20 digits
    """,

    'author': "Itsys-corportion Eman Ahmed",
    'website': "www.it-syscorp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account_invoicing'],
    'data':[
        'views/currency_rate.xml',
    ]


}