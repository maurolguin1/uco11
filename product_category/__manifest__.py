# -*- coding: utf-8 -*-
{
    'name': "Product Category",

    'summary': """
        confirm product by product manager""",

    'description': """
        confirm product by product manager
    """,

    'author': "ITsys-Corportion Eman ahmed",
    'website': "http://www.it-syscorp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','product','hr','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_category.xml',
    ],
    # only loaded in demonstration mode

}