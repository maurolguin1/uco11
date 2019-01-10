# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.model
    def create(self, vals):
        if vals.get('team_id'):
            vals.update(item for item in
                        self._onchange_team_get_values(self.env['helpdesk.team'].browse(vals['team_id'])).items() if
                        item[0] not in vals)
        print ("aaaaaaaa")
        # context: no_log, because subtype already handle this
        ticket = super(HelpdeskTicket, self.with_context(mail_create_nolog=False)).create(vals)
        print ("ticket",ticket)
        if ticket.partner_id:
            ticket.message_subscribe(partner_ids=ticket.partner_id.ids)
            ticket._onchange_partner_id()
        if ticket.user_id:
            ticket.assign_date = ticket.create_date
            ticket.assign_hours = 0

        return ticket

