
from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    restrict_records_number = fields.Boolean(string="Restrict Records Number")

