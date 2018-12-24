# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    manager_id = fields.Many2one('res.users', string='Product Manager', readonly=True)
    state_confirm = fields.Selection([
        ('confirm', 'Confirm')], store=True)


    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if self.product_id:
            self.manager_id = self.product_id.categ_id.manager_id.id
        return res

    @api.multi
    @api.onchange('state_confirm')
    def _check_manager(self):
        for line in self:
            if line.product_id:
                if self.env.user.has_group('base.group_system'):
                    print("admin")
                    pass
                elif line.product_id.categ_id.manager_id:
                    print("product manager for product ")
                    if line.manager_id:
                        print('product manager for line')
                        if line.manager_id.id != self.env.user.id:
                            raise ValidationError("PM Should Confirm")
                        else:
                            print("CONFIRMED")
                elif not line.product_id.categ_id.manager_id:
                    print("not product manager for product")
                    if line.manager_id:
                        print('product manager for line')
                        if line.manager_id.id != self.env.user.id:
                            raise ValidationError("PM Should Confirm")
                        else:
                            print("CONFIRMED")


# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     @api.multi
#     @api.constrains('order_line')
#     def _check_manager(self):
#         print("onchange")
#         for rec in self:
#             for line in rec.order_line:
#                 print(line)
#                 if line.product_id:
#                     if self.env.user.has_group('base.group_system'):
#                         print("admin")
#                         pass
#                     elif line.product_id.categ_id.manager_id:
#                         print("product manager for product ")
#                         if line.manager_id:
#                             print('product manager for line')
#                             if line.manager_id.id != self.env.user.id:
#                                 raise ValidationError("PM Should Confirm")
#                     elif not line.product_id.categ_id.manager_id:
#                         print("not product manager for product")
#                         if line.manager_id:
#                             print('product manager for line')
#                             if line.manager_id.id != self.env.user.id:
#                                 raise ValidationError("PM Should Confirm")