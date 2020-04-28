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
        if context.get('start_task') and context.get('active_model') == 'maintenance.request':
            result.update({'name': "Are you going to start the task " })
        if context.get('continue_task') and context.get('active_model') == 'maintenance.request':
            result.update({'name': "Are you going to continue the task " })
        if context.get('restart_task') and context.get('active_model') == 'maintenance.request':
            result.update({'name': "Are you going to restart the task " })
        return result

    '''@api.multi
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
                if maintenance_ids[0].start_datetime != False and maintenance_ids[0].con_time == False:
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(maintenance_ids.start_datetime), '%Y-%m-%d %H:%M:%S')
                if maintenance_ids[0].con_time != False:
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(maintenance_ids.con_time), '%Y-%m-%d %H:%M:%S')

                m, s = divmod(pausetime_diff.total_seconds(), 60)
                h, m = divmod(m, 60)
                dur_h = (_('%0*d') % (2, h))
                dur_m = (_('%0*d') % (2, m * 1.677966102))
                dur_s = (_('%0*d') % (2, s))
                duration = dur_h + '.' + dur_m + '.' + dur_s
                hr_duration = dur_h + '.' + dur_m
                amount = float(hr_duration)
                timesheet_vals = {

                    'name': self.description,
                    'date': start_date,
                    'amount': amount,
                    'account_id': account_id,
                    'employee_id': emp_id,
                    'time': duration
                }
                maintenance_ids.write({'state': 'end', 'end_datetime': p_time, 'timesheet_ids': [(0, 0, timesheet_vals)]})
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

                    'name': self.description,
                    'date': start_date,
                    'amount': amount,
                    'account_id': account_id,
                    'employee_id': emp_id,
                    'time': duration
                }
                maintenance_ids.write({'state': 'in_process', 'con_time':p_time,'timesheet_ids': [(0, 0, timesheet_vals)]})
        return True'''

    @api.multi
    def accept_task(self):
        context = self._context
        print ("^^^^^^^context^^^^^^^^^",context)
        maintenance_ids = self.env['maintenance.request'].sudo().search([('id', '=', context.get('active_id'))])
        data_list = []
        start_date = datetime.today()
        account_id = self.env.ref('canet_maintenance.analytic_account_maintenance_id', False).id
        p_time = fields.Datetime.now()
        '''if project_task:
            if not project_task.project_id:
                raise UserError(_("Por favor asigne Proyecto primero"))'''
        if context.get('ok') and context.get('start_task') and context.get('active_model') == 'maintenance.request' :
            if maintenance_ids:
                maintenance_ids.write({'state': 'start', 'start_time': p_time, 'start_date': start_date})
        if context.get('ok') and context.get('restart_task') and context.get('active_model') == 'maintenance.request':
            if maintenance_ids:
                maintenance_ids.write({'state': 'start', 'restart_time': p_time, 'start_date': start_date})
        if context.get('ok') and context.get('continue_task') and context.get('active_model') == 'maintenance.request':
            if maintenance_ids:
                maintenance_ids.write({'state': 'continue', 'con_time': p_time, 'start_date': start_date})
        if context.get('ok') and context.get('end_task') and context.get('active_model') == 'maintenance.request':
            if maintenance_ids.start_time != False and maintenance_ids.con_time == False and maintenance_ids.restart_time == False:
                start_time = maintenance_ids.start_time
                endtime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(maintenance_ids.start_time), '%Y-%m-%d %H:%M:%S')
            if maintenance_ids.restart_time != False and maintenance_ids.con_time == False:
                start_time = maintenance_ids.restart_time
                endtime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(maintenance_ids.restart_time), '%Y-%m-%d %H:%M:%S')
            if maintenance_ids.con_time != False and maintenance_ids.restart_time == False:
                start_time = maintenance_ids.con_time
                endtime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(maintenance_ids.con_time), '%Y-%m-%d %H:%M:%S')
            if maintenance_ids.restart_time != False and maintenance_ids.con_time != False:
                start_time = maintenance_ids.restart_time
                endtime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(maintenance_ids.restart_time), '%Y-%m-%d %H:%M:%S')
            print("---------------------", endtime_diff)
            m, s = divmod(endtime_diff.total_seconds(), 60)
            h, m = divmod(m, 60)
            dur_h = (_('%0*d') % (2, h))
            dur_m = (_('%0*d') % (2, m * 1.677966102))
            dur_s = (_('%0*d') % (2, s))
            duration = dur_h + '.' + dur_m + '.' + dur_s
            print("<<<<<<<duration<<<<<<<", duration)
            data = {'name': self.description,
                    'date': datetime.now(),
                    'start_date': start_time if maintenance_ids else '',
                    'time': duration,
                    'account_id': account_id,
                    'user_id': self._uid}
            data_list.append((0, 0, data))
            maintenance_ids.write({'state': 'end', 'timesheet_ids': data_list})
        if context.get('ok') and context.get('stop_task') and context.get('active_model') == 'maintenance.request':
            if maintenance_ids.start_time != False and maintenance_ids.con_time == False and maintenance_ids.restart_time == False:
                start_time = maintenance_ids.start_time
                stoptime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(maintenance_ids.start_time), '%Y-%m-%d %H:%M:%S')
            if maintenance_ids.restart_time != False and maintenance_ids.con_time == False:
                start_time = maintenance_ids.restart_time
                stoptime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(maintenance_ids.restart_time), '%Y-%m-%d %H:%M:%S')
            if maintenance_ids.con_time != False and maintenance_ids.restart_time == False:
                start_time = maintenance_ids.con_time
                stoptime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(maintenance_ids.con_time), '%Y-%m-%d %H:%M:%S')
            if maintenance_ids.restart_time != False and maintenance_ids.con_time != False:
                start_time = maintenance_ids.restart_time
                stoptime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(maintenance_ids.restart_time), '%Y-%m-%d %H:%M:%S')
            if maintenance_ids.start_time == False and maintenance_ids.con_time == False and maintenance_ids.restart_time == False:
                start_time = p_time
                stoptime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(p_time),
                                                                                                        '%Y-%m-%d %H:%M:%S')
            m, s = divmod(stoptime_diff.total_seconds(), 60)
            h, m = divmod(m, 60)
            dur_h = (_('%0*d') % (2, h))
            dur_m = (_('%0*d') % (2, m * 1.677966102))
            dur_s = (_('%0*d') % (2, s))
            duration = dur_h + '.' + dur_m + '.' + dur_s
            data = {'name': self.description,
                    'date': datetime.now(),
                    'start_date': start_time if maintenance_ids else '',
                   # 'project_id': project_task.project_id.id,
                   # 'task_id': project_task.id,
                    'time': duration,
                    'account_id': account_id,
                    'user_id': self._uid}
            data_list.append((0, 0, data))
            maintenance_ids.write({'state': 'stop', 'timesheet_ids': data_list})
        return True