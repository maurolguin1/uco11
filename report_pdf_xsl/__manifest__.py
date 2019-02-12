# -*- coding: utf-8 -*-
{
    'name': "report pdf, xsl",

    'summary': """
        report pdf, xsl""",

    'description': """
       report pdf, xsl
    """,

    'author': "ITsys-Corportion Eman ahmed",
    'website': "http://www.it-syscorp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','report_xlsx',],

    # always loaded
    'data': [
        'report/report.xml',
        'report/report_saleorder.xml',
        'views/sale_order.xml',
    ],
    # only loaded in demonstration mode

}