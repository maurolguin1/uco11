# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):
    _inherit = 'product.category'

    managers_id = fields.Many2many('res.users', string='Product Managers')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    state_confirm = fields.Selection([
        ('c', 'Confirm')], store=True)

    @api.depends('product_id')
    def _get_prodcut_managers(self):
        for rec in self:
            if rec.product_id:
                if rec.product_id.categ_id.managers_id:
                    rec.managers_id = rec.product_id.categ_id.managers_id

    managers_id = fields.Many2many('res.users', compute="_get_prodcut_managers", string='Product Managers', store=True)


    @api.multi
    @api.onchange('state_confirm')
    def _check_manager(self):
        for line in self:
            if line.product_id:
                if self.env.user.has_group('base.group_system'):
                    pass
                elif line.managers_id:
                    if self.env.user.id not in line.managers_id.ids:
                        raise ValidationError("PM Should Confirm")