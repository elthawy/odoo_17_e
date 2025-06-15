from odoo import models, fields
from odoo.exceptions import ValidationError
import base64
import io
import xlsxwriter

class SaleReportWizard(models.TransientModel):
    _name = 'sale.report.wizard'
    _description = 'Sale Report Wizard'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)
    customer_id = fields.Many2one('res.partner', string="Customer", required=True)

    def action_print_xlsx(self):
        if self.date_from > self.date_to:
            raise ValidationError("Start date must be before end date.")

        domain = [
            ('date_order', '>=', self.date_from),
            ('date_order', '<=', self.date_to),
            ('partner_id', '=', self.customer_id.id)
        ]
        orders = self.env['sale.order'].search(domain)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Customer Orders')

        # تنسيقات
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#CFE2F3',  # لون العنوان
            'border': 1,
            'align': 'center'
        })
        row_green = workbook.add_format({'bg_color': '#E2F0D9', 'border': 1})
        row_white = workbook.add_format({'bg_color': '#FFFFFF', 'border': 1})

        # العناوين
        headers = ['Reference', 'Customer', 'Date', 'Phone', 'Email',
                   'Number of Products', 'State', 'Total']
        for col, h in enumerate(headers):
            sheet.write(0, col, h, header_format)

        # البيانات
        for row, order in enumerate(orders, start=1):
            fmt = row_green if row % 2 == 1 else row_white
            sheet.write(row, 0, order.name, fmt)
            sheet.write(row, 1, order.partner_id.name or '', fmt)
            sheet.write(row, 2, order.date_order.strftime('%Y-%m-%d') if order.date_order else '', fmt)
            sheet.write(row, 3, order.partner_id.phone or '', fmt)
            sheet.write(row, 4, order.partner_id.email or '', fmt)
            sheet.write(row, 5, len(order.order_line), fmt)
            sheet.write(row, 6, order.state, fmt)
            sheet.write(row, 7, order.amount_total, fmt)

        workbook.close()
        output.seek(0)

        attachment = self.env['ir.attachment'].create({
            'name': 'customer_sale_report.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'res_model': 'sale.report.wizard',
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self'
        }