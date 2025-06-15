from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    records_number = fields.Integer(string="Number of Duplicates")
    records_number_readonly = fields.Boolean(
        compute='_compute_records_number_readonly',
        store=False,
        string="Readonly Status"
    )

    @api.depends('records_number')
    def _compute_records_number_readonly(self):
        group = self.env.ref('sales_order_duplicator.group_restrict_records_number', raise_if_not_found=False)
        for rec in self:
            if group:
                rec.records_number_readonly = not (self.env.user in group.users)
            else:
                rec.records_number_readonly = False