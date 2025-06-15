from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError
from odoo.tools import safe_eval
import re

class SalesTechnical(models.Model):
    _name = 'sales.technical'
    _description = 'Sales Technical Operations'

    name = fields.Char('Title', default='Technical ORM/SQL Executor')
    code = fields.Text(
        string='Command',
        help="Example ORM: env['sale.order'].search([])\nExample SQL: SELECT name FROM sale_order LIMIT 5"
    )
    result = fields.Text(string='Execution Result', readonly=True)

    @api.model
    def check_access_rights(self, operation, raise_exception=True):
        if not self.env.user.has_group('base.group_no_one'):
            if raise_exception:
                raise AccessError("This feature requires Developer Mode!")
            return False
        return super().check_access_rights(operation, raise_exception)

    def is_sql_query(self, code):
        return bool(re.match(r'^\s*(SELECT|UPDATE|DELETE|INSERT)', code.strip(), re.IGNORECASE))

    def execute_orm(self):
        self.ensure_one()
        if self.is_sql_query(self.code):
            raise UserError("❌ This appears to be a SQL query. Use the 'Execute SQL' button instead.")

        try:
            allowed_locals = {
                'env': self.env,
                'user': self.env.user,
                'model': self,
                'record': self,
            }

            result = safe_eval.safe_eval(self.code.strip(), allowed_locals)

            if isinstance(result, models.BaseModel):
                self.result = f"✅ Found {len(result)} records:\n{result.mapped('display_name')}"
            elif isinstance(result, (list, dict, set)):
                self.result = f"✅ Result:\n{str(result)}"
            else:
                self.result = f"✅ Result: {str(result)}"

        except Exception as e:
            self.result = f"❌ ORM Error: {str(e)}"

    def execute_sql(self):
        self.ensure_one()
        if not self.is_sql_query(self.code):
            raise UserError("❌ This appears to be an ORM expression. Use the 'Execute ORM' button instead.")

        try:
            self.env.cr.execute(self.code.strip())
            if self.env.cr.description:
                columns = [col[0] for col in self.env.cr.description]
                rows = self.env.cr.fetchall()
                result_text = '\n'.join([str(dict(zip(columns, row))) for row in rows])
                self.result = f"✅ SQL Result:\n{result_text}"
            else:
                self.result = "✅ SQL query executed successfully. (No return data)"

        except Exception as e:
            self.result = f"❌ SQL Error: {str(e)}"

    def action_save(self):
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel(self):
        self.write({'code': '', 'result': ''})
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'current',
        }
