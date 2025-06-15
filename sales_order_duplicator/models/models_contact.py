from odoo import models

class SaleOrderDuplicate(models.Model):
    _inherit = 'sale.order'

    def action_duplicate_records(self):
        for order in self:
            num = order.records_number
            if num > 1:
                for i in range(num - 1):
                    values = order.copy_data()[0]
                    values.pop('name', None)
                    self.env['sale.order'].create(values)
