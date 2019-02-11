# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'



    @api.model
    def create(self, vals):
        if 'order_line' not in vals:
            raise UserError("Please add lines in Quotation")
        res = super(SaleOrder, self.sudo()).create(vals)
        return res

    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self.sudo()).write(vals)
        return res

    total_state = fields.Char('Total State', compute='calc_state', store=True)

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('confirmed_line', 'Confirmed'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    @api.constrains('total_state')
    def change_state(self):
        for line in self:
            if line.total_state == 'Confirm Complate':
                line.state = 'confirmed_line'
            elif line.total_state == 'Waiting Confirm' or line.total_state == ' ':
                line.state = 'draft'



    @api.depends('order_line.state_confirm')
    def calc_state(self):
        list = []
        for line in self:
            if line.order_line:
                for rec in line.order_line:
                    list.append(rec.state_confirm)

            print (list)

            if list.count(False) > 0:
                line.total_state = 'Waiting Confirm'

            elif list.count(False) == 0 and list.count('confirm') == 0:

                line.total_state = ' '
            else:

                line.total_state = 'Confirm Complate'


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self.sudo()).create(vals)
        return res

    @api.multi
    def write(self, vals):
        res = super(SaleOrderLine, self.sudo()).write(vals)
        return res

    @api.depends("product_id")
    def _get_prodcut_managers(self):
        for rec in self:
            if rec.product_id:
                if rec.product_id.categ_id.managers_id:
                    rec.managers_id = rec.product_id.categ_id.managers_id

    managers_id = fields.Many2many('res.users', compute="_get_prodcut_managers", string='Product Managers', store=True)

    state_confirm = fields.Selection([
        ('confirm', 'Confirm')], store=True)

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










