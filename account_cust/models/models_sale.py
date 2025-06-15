from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sequence_number = fields.Integer(
        string="No.",
        compute='_compute_sequence_number',
        store=True,
        readonly=True
    )



    @api.depends('move_id.invoice_line_ids')
    def _compute_sequence_number(self):
        for order in self.mapped('move_id'):
            for index, line in enumerate(order.invoice_line_ids, start=1):
                line.sequence_number= index * 1
                print('index')
