
from odoo import models, fields, api
from datetime import date

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        if vals.get('move_type') in ('out_invoice', 'out_refund') and not vals.get('name'):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            code = partner.contact_code or 'CUST'
            seq = self.env['ir.sequence'].next_by_code('custom.invoice.sequence') or '/'
            year = date.today().year
            vals['name'] = f"{code}/{year}/{seq}"
        return super().create(vals)
