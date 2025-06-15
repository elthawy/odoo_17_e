from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    mobile_number  = fields.Char(
        string="Phone",
        related='partner_id.phone',
        store=True,
        readonly=True
    )











