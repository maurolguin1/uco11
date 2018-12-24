# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):
    _inherit = 'product.category'

    manager_id = fields.Many2one('res.users', string='Product Manager')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    state_confirm = fields.Selection([
        ('c', 'Confirm')], store=True)

    product_manager_id = fields.Many2one('res.users', string='Product Manager')

    @api.multi
    @api.onchange('product_id')
    def onchange_product_id(self):
        res = super(PurchaseOrderLine, self).onchange_product_id()
        if self.product_id:
            self.product_manager_id = self.product_id.categ_id.manager_id.id
        return res

    @api.multi
    @api.onchange('state_confirm')
    def _check_manager(self):
        for line in self:
            if line.product_id:
                if self.env.user.has_group('base.group_system'):
                    pass
                elif line.product_id.categ_id.manager_id:
                    if line.product_manager_id:
                        if line.product_manager_id.id != self.env.user.id:
                            raise ValidationError("PM Should Confirm")
                        else:
                            print("CONFIRMED")
                elif not line.product_id.categ_id.manager_id:
                    print("not product manager for product")
                    if line.product_manager_id:
                        print('product manager for line')
                        if line.product_manager_id.id != self.env.user.id:
                            raise ValidationError("PM Should Confirm")
                        else:
                            print("CONFIRMED")


# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'

    # total_state = fields.Char('Total State', compute='calc_state', store=True)
    #
    # state = fields.Selection([
    #     ('draft', 'RFQ'),
    #     ('sent', 'RFQ Sent'),
    #     ('to approve', 'To Approve'),
    #     ('w', 'Waiting PM Confirmation'),
    #     ('purchase', 'Purchase Order'),
    #     ('done', 'Locked'),
    #     ('cancel', 'Cancelled')
    # ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange',
    #     compute='change_state', store=True)

    # @api.multi
    # @api.constrains('order_line')
    # def _check_manager(self):
    #     print("onchange po")
    #     for rec in self:
    #         for line in rec.order_line:
    #             print(line)
    #             if line.product_id:
    #                 if self.env.user.has_group('base.group_system'):
    #                     pass
    #                 elif line.product_id.categ_id.manager_id:
    #                     print("product manager for product ")
    #                     if line.product_manager_id:
    #                         print('product manager for line')
    #                         if line.product_manager_id.id != self.env.user.id:
    #                             raise ValidationError("PM Should Confirm")
    #                 elif not line.product_id.categ_id.manager_id:
    #                     print("not product manager for product")
    #                     if line.product_manager_id:
    #                         print('product manager for line')
    #                         if line.product_manager_id.id != self.env.user.id:
    #                             raise ValidationError("PM Should Confirm")

    # @api.depends('total_state')
    # def change_state(self):
    #     for line in self:
    #         if line.total_state == ' ' or line.total_state == 'Confirm Complate':
    #             line.state = 'draft'
    #         elif line.total_state == 'Waiting Confirm':
    #             line.state = 'w'

    # @api.depends('order_line.state')
    # def calc_state(self):
    #     list = []
    #     for line in self:
    #         if line.order_line:
    #             for rec in line.order_line:
    #                 list.append(rec.state_confirm)
    #
    #         if list.count(False) > 0:
    #             line.total_state = 'Waiting Confirm'
    #
    #         elif list.count(False) == 0 and list.count('c') == 0:
    #
    #             line.total_state = ' '
    #         else:
    #
    #             line.total_state = 'Confirm Complate'
