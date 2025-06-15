from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sequence = fields.Integer(
        string='Sequence',
        default=0,
        compute='_compute_sequence',
        store=True,
        readonly=False
    )

    @api.depends('order_id.order_line')
    def _compute_sequence(self):
        for order in self.mapped('order_id'):
            for index, line in enumerate(order.order_line, start=1):
                line.sequence = index * 1






