from odoo import models, fields


class AccountAgedReceivable(models.Model):
    _inherit = 'account.aged.receivable'  # توريث النموذج الأصلي

    # تعريف الحقل الجديد من نوع Char
    custom_field = fields.Char(
        string="حقل مخصص",  # التسمية التي تظهر في الواجهة
        help="هذا حقل مخصص يظهر بعد تاريخ الاستحقاق"  # نص مساعد
    )








