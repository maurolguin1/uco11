# -*- coding: utf-8 -*-
{
    'name': "Product Manager Security",

    'summary': """Product Manager Security""",

    'description': """Product Manager Security""",

    'author': "ITSYS By Shimaa",
    'website': "http://www.it-syscorp.com",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['product_category','sale'],
    'data': [
        'security/sale_order_security.xml',
        'security/ir.model.access.csv',
        'views/sale_order.xml',
    ],
}