# -*- coding: utf-8 -*-
{
    'name': "Product Manager Security",

    'summary': """Product Manager Security""",

    'description': """Product Manager Security""",

    'author': "ITSYS By ALShimaa",
    'website': "http://www.it-syscorp.com",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['product_category', 'purchase', 'sale','sale_stock'],
    'data': [

        'security/sale_order_security.xml',
        'views/sale_order.xml',
    ],
}
