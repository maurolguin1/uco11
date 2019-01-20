# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CurrencyRate(models.Model):
    _inherit = "res.currency.rate"


    rate = fields.Float(digits=(12,16), help='The rate of the currency to the currency of rate 1')





