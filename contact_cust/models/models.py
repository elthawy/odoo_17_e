from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    contact_code = fields.Char(
        required=False,
        copy=False,
        index=True
    )

    @api.model
    def create(self, vals):
        if not vals.get('contact_code'):
            vals['contact_code'] = self.env['ir.sequence'].next_by_code('res.partner.contact.code')
        return super().create(vals)
