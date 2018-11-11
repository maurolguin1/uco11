# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductCategory(models.Model):
    _inherit ='product.category'

    product_manager_id= fields.Many2one('hr.employee',string='Product Manager')





class PurchaseOrderLine(models.Model):
    _inherit ='purchase.order.line'
    state=fields.Boolean(store=True,compute='check_employee')

    state_confirm=fields.Selection([
        ('c','Confirm')
    ],store=True)


    @api.onchange('state_confirm')
    def change_state(self):
        for line in self:
          if line.state_confirm =='c' and line.state==False:
            raise ValidationError("PM Should Confirm ")

    product_manager_id= fields.Many2one('hr.employee',string='Product Manager',related='product_id.categ_id.product_manager_id',store=True,readonly=True)
    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)

    @api.depends('product_manager_id')
    def check_employee(self):
        for line in self:
            for l in line.current_user.employee_ids:
                if line.product_manager_id == l:
                    line.state=True






class PurchaseOrder(models.Model):
    _inherit ='purchase.order'
    total_state=fields.Char('Total State',compute='calc_state',store=True)



    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('w', 'Waiting PM Confirmation'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange',compute='change_state',store=True)


    @api.depends('total_state')
    def change_state(self):
        for line in self:
            if line.total_state==' ' or line.total_state =='Confirm Complate' :
                line.state = 'draft'
            elif line.total_state=='Waiting Confirm':
                line.state='w'



    @api.depends('order_line.state')
    def calc_state(self):
        list=[]
        for line in self:
            if line.order_line:
                for rec in  line.order_line:
                    list.append(rec.state_confirm)

            if list.count(False)>0:
                line.total_state = 'Waiting Confirm'

            elif list.count(False)==0 and list.count('c')==0:

                line.total_state = ' '
            else:

                line.total_state = 'Confirm Complate'





