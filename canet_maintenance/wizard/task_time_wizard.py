from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError

import time
import pytz


# create new wizard object for manage task(start,end,stop)
class TaskTimeWizard(models.TransientModel):
    _name = 'task.time.wizard'

    name = fields.Char(string="Name")
    description = fields.Text("Description")

    @api.model
    def default_get(self, vals):
        result = super(TaskTimeWizard, self).default_get(vals)
        context = self.env.context
        wash_obj = self.env['maintenance.request'].search([('id', '=', context.get('active_id'))])
        if context.get('start_process'):
            result.update({'name': "Are you sure You want to start Process?"})
        if context.get('stop_process'):
            result.update({'name': "Are you sure You want to Stop Process?"})
        if context.get('continue_process'):
            result.update({'name': "Are you sure You want to Continue Process?"})
        return result

    @api.multi
    def accept_task(self):
        context = self._context
        maintenance_ids = self.env['maintenance.request'].sudo().search([('id', '=', context.get('active_id'))])
        data_list = []
        user_tz = self.env.user.tz
        local = pytz.timezone(user_tz)
        start_date = datetime.today()
        p_time = fields.Datetime.now(local)
        amount = 0.0
        emp_id = False
        emp_id = self.env['hr.employee'].search([('user_id', '=', self._uid)])
        if emp_id:
            emp_id = emp_id.id
        account_id = self.env.ref('canet_maintenance.analytic_account_maintenance_id', False).id
        if context.get('ok') and context.get('start_process') :
            if maintenance_ids:
                maintenance_ids.write({'state': 'in_process', 'start_datetime': p_time})
        if context.get('ok') and context.get('stop_process') :
            if maintenance_ids:
                pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(maintenance_ids.start_datetime), '%Y-%m-%d %H:%M:%S')
                m, s = divmod(pausetime_diff.total_seconds(), 60)
                h, m = divmod(m, 60)
                dur_h = (_('%0*d') % (2, h))
                dur_m = (_('%0*d') % (2, m * 1.677966102))
                dur_s = (_('%0*d') % (2, s))
                duration = dur_h + '.' + dur_m + '.' + dur_s
                hr_duration = dur_h + '.' + dur_m
                amount = float(hr_duration)
                timesheet_vals = {

                    'name': 'Process Time',
                    'date': start_date,
                    'amount': amount,
                    'account_id': account_id,
                    'employee_id': emp_id,
                    'time': duration
                }
                maintenance_ids.write({'state': 'to_repair', 'end_datetime': p_time, 'timesheet_ids': [(0, 0, timesheet_vals)]})
        if context.get('ok') and context.get('continue_process') :
            if maintenance_ids:
                pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(maintenance_ids.end_datetime), '%Y-%m-%d %H:%M:%S')
                m, s = divmod(pausetime_diff.total_seconds(), 60)
                h, m = divmod(m, 60)
                dur_h = (_('%0*d') % (2, h))
                dur_m = (_('%0*d') % (2, m * 1.677966102))
                dur_s = (_('%0*d') % (2, s))
                duration = dur_h + '.' + dur_m + '.' + dur_s
                hr_duration = dur_h + '.' + dur_m
                amount = float(hr_duration)
                timesheet_vals = {

                    'name': 'Repair Time',
                    'date': start_date,
                    'amount': amount,
                    'account_id': account_id,
                    'employee_id': emp_id,
                    'time': duration
                }
                maintenance_ids.write({'state': 'in_process', 'timesheet_ids': [(0, 0, timesheet_vals)]})
        return True
