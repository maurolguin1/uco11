# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    manager_id = fields.Many2one('res.users', string='Product Manager', related='product_id.categ_id.manager_id', store=True, readonly=True)

    state_confirm = fields.Selection([
        ('confirm', 'Confirm')], store=True)

    @api.multi
    @api.onchange('state_confirm')
    def _check_manager(self):
        for line in self:
            if line.product_id:
                if self.env.user.has_group('base.group_system'):
                    pass
                elif line.manager_id:
                    if line.manager_id.id != self.env.user.id:
                        raise ValidationError("PM Should Confirm")

