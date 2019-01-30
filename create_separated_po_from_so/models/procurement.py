# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
from odoo.addons import decimal_precision as dp


class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    def get_price_unit(self,origin,product_id):
        sale_id=False
        price_unit=False
        supplier_id=False
        supplier_info=False
        discount=False
        create_po=False
        interest_id=False
        advance_payment=False

        for each_sale in self.env['sale.order'].search([('name', '=', origin)]):
            sale_id=each_sale.id
            supplier_id=each_sale.supplier_id
        if sale_id:
            for each_sale_line in self.env['sale.order.line'].search([('order_id', '=', sale_id),('product_id', '=', product_id.id)]):
                price_unit = each_sale_line.price_unit
                # discount=each_sale_line.discount
                # create_po=each_sale_line.create_po
                # interest_id=each_sale_line.interest_id
                # advance_payment=each_sale_line.advance_payment

        if supplier_id:

            for each_info in self.env['product.supplierinfo'].search([('name', '=', supplier_id.id),('product_id','=',product_id.id)]):
                supplier_info=each_info
            if not supplier_info:
                supplierinfo_vals = {
                    'name': supplier_id.id,
                    'price': price_unit,
                    'product_id':product_id.id,
                }

                supplier_info = self.env["product.supplierinfo"].create(supplierinfo_vals)

        return price_unit,supplier_info,discount

    @api.multi
    def _run_buy(self, product_id, product_qty, product_uom, location_id, name, origin, values):
        cache = {}
        suppliers = product_id.seller_ids\
            .filtered(lambda r: (not r.company_id or r.company_id == values['company_id']) and (not r.product_id or r.product_id == product_id))
        if not suppliers:
            msg = _('There is no vendor associated to the product %s. Please define a vendor for this product.') % (product_id.display_name,)
            raise UserError(msg)

        supplier = self._make_po_select_supplier(values, suppliers)
        create_po=False
        interest_id=False
        p,s,discount = self.get_price_unit(origin, product_id)

        if s:
            supplier = s
        partner = supplier.name

        domain = self._make_po_get_domain(values, partner)

        if domain in cache:
            po = cache[domain]
        else:
            po = self.env['purchase.order'].search([dom for dom in domain])
            po = po[0] if po else False
            cache[domain] = po
        po=False
        # po = self.env['purchase.order'].search([('sale_id','=',sale_id)])
        # po = po[0] if po else False
        if not po:
            vals = self._prepare_purchase_order(product_id, product_qty, product_uom, origin, values, partner)

            po = self.env['purchase.order'].create(vals)
            cache[domain] = po
            # so= self.env['sale.order'].browse(sale_id)
            # so.write({'purchase_id':po.id})
        elif not po.origin or origin not in po.origin.split(', '):
            if po.origin:
                if origin:
                    po.write({'origin': po.origin + ', ' + origin})
                else:
                    po.write({'origin': po.origin})
            else:
                po.write({'origin': origin})

        # Create Line
        po_line = False
        if not po_line:
            vals = self._prepare_purchase_order_line1(product_id, product_qty, product_uom, values, po, supplier,p,discount)
            self.env['purchase.order.line'].create(vals)

    @api.multi
    def _prepare_purchase_order_line1(self, product_id, product_qty, product_uom, values, po, supplier,price_unit=False,discount=False):
        procurement_uom_po_qty = product_uom._compute_quantity(product_qty, product_id.uom_po_id)
        seller = product_id._select_seller(
            partner_id=supplier.name,
            quantity=procurement_uom_po_qty,
            date=po.date_order and po.date_order[:10],
            uom_id=product_id.uom_po_id)
        seller=supplier
        taxes = product_id.supplier_taxes_id
        fpos = po.fiscal_position_id
        taxes_id = fpos.map_tax(taxes) if fpos else taxes
        if taxes_id:
            taxes_id = taxes_id.filtered(lambda x: x.company_id.id == values['company_id'].id)
        pp=seller.price
        if price_unit:
            pp=price_unit
        price_unit = self.env['account.tax']._fix_tax_included_price_company(pp, product_id.supplier_taxes_id, taxes_id, values['company_id']) if seller else 0.0
        if price_unit and seller and po.currency_id and seller.currency_id != po.currency_id:
            price_unit = seller.currency_id.compute(price_unit, po.currency_id)

        product_lang = product_id.with_context({
            'lang': supplier.name.lang,
            'partner_id': supplier.name.id,
        })
        name = product_lang.display_name
        if product_lang.description_purchase:
            name += '\n' + product_lang.description_purchase

        date_planned = self.env['purchase.order.line']._get_date_planned(seller, po=po).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        return {
            'name': name,
            'product_qty': procurement_uom_po_qty,
            'product_id': product_id.id,
            'product_uom': product_id.uom_po_id.id,
            'price_unit': price_unit,
            'date_planned': date_planned,
            'orderpoint_id': values.get('orderpoint_id', False) and values.get('orderpoint_id').id,
            'taxes_id': [(6, 0, taxes_id.ids)],
            'order_id': po.id,
            # 'discount': discount,
            # 'interest_id': [(6, 0, interest_id.ids)],
            # 'advance_payment':advance_payment,
            'move_dest_ids': [(4, x.id) for x in values.get('move_dest_ids', [])],
        }
