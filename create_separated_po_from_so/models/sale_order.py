# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class salesorder(models.Model):
    _inherit = "sale.order"
    supplier_id = fields.Many2one(comodel_name='res.partner',domain=[('supplier','=',True)], string='Supplier')
class salesorderline(models.Model):
    _inherit = "sale.order.line"
    create_po = fields.Boolean('Create PO',default=True)
