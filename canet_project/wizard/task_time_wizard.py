from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError

import time
import pytz


# create new wizard object for manage task(start,end,stop)
class TaskTimeWizard(models.TransientModel):
    _inherit = 'task.time.wizard'

    @api.model
    def default_get(self, vals):
        result = super(TaskTimeWizard, self).default_get(vals)
        context = self.env.context
        project_task = self.env['project.task'].search([('id', '=', context.get('active_id'))])
        if context.get('start_task'):
            result.update({'name': "Are you going to start the task " + project_task.name + '?'})
        if context.get('continue_task'):
            result.update({'name': "Are you going to continue the task " + project_task.name + '?'})
        if context.get('restart_task'):
            result.update({'name': "Are you going to restart the task " + project_task.name + '?'})
        return result

    @api.multi
    def accept_task(self):
        context = self._context
        result = super(TaskTimeWizard, self).accept_task()
        project_task = self.env['project.task'].sudo().search([('id', '=', context.get('active_id'))])
        data_list = []
        start_date = datetime.today()
        p_time = fields.Datetime.now()
        if project_task:
            if not project_task.project_id:
                raise UserError(_("Por favor asigne Proyecto primero"))
        if context.get('ok') and context.get('start_task'):
            if project_task:
                project_task.write({'state': 'start', 'start_time': p_time, 'start_date': start_date})
        if context.get('ok') and context.get('restart_task'):
            if project_task:
                project_task.write({'state': 'start', 'restart_time': p_time, 'start_date': start_date})
        if context.get('ok') and context.get('continue_task'):
            if project_task:
                project_task.write({'state': 'continue', 'con_time': p_time, 'start_date': start_date})
        if context.get('ok') and context.get('end_task'):

            if project_task.start_time != False and project_task.con_time == False and project_task.restart_time == False:
                start_time = project_task.start_time
                endtime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(project_task.start_time), '%Y-%m-%d %H:%M:%S')
            if project_task.restart_time != False and project_task.con_time == False:
                start_time = project_task.restart_time
                endtime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(project_task.restart_time), '%Y-%m-%d %H:%M:%S')
            if project_task.con_time != False and project_task.restart_time == False:
                start_time = project_task.con_time
                endtime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(project_task.con_time), '%Y-%m-%d %H:%M:%S')
            if project_task.restart_time != False and project_task.con_time != False:
                start_time = project_task.restart_time
                endtime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(project_task.restart_time), '%Y-%m-%d %H:%M:%S')
            print ("---------------------",endtime_diff)
            m, s = divmod(endtime_diff.total_seconds(), 60)
            h, m = divmod(m, 60)
            dur_h = (_('%0*d') % (2, h))
            dur_m = (_('%0*d') % (2, m * 1.677966102))
            duration = dur_h + '.' + dur_m
            print ("<<<<<<<duration<<<<<<<",duration)
            data = {'name': self.description,
                    'date': datetime.now(),
                    'start_date': start_time if project_task else '',
                    'project_id': project_task.project_id.id,
                    'task_id': project_task.id,
                    'unit_amount': float(duration),
                    'user_id': self._uid}
            data_list.append((0, 0, data))
            marivi_user_id = self.env['res.users'].search([('login', '=', 'oroval.servicios.adm@gmail.com')])
            project_task.write({'state': 'end', 'timesheet_ids': data_list, 'user_id': marivi_user_id.id})
            get_task = [task.id for task in project_task.project_id.task_ids if task.state == 'end']
        if context.get('ok') and context.get('stop_task'):
            if project_task.start_time != False and project_task.con_time == False and project_task.restart_time == False:
                start_time = project_task.start_time
                stoptime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(project_task.start_time), '%Y-%m-%d %H:%M:%S')
            if project_task.restart_time != False and project_task.con_time == False:
                start_time = project_task.restart_time
                stoptime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(project_task.restart_time), '%Y-%m-%d %H:%M:%S')
            if project_task.con_time != False and project_task.restart_time == False:
                start_time = project_task.con_time
                stoptime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(project_task.con_time), '%Y-%m-%d %H:%M:%S')
            if project_task.restart_time != False and project_task.con_time != False:
                start_time = project_task.restart_time
                stoptime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                    str(project_task.restart_time), '%Y-%m-%d %H:%M:%S')
            if project_task.start_time == False and project_task.con_time == False and project_task.restart_time == False:
                start_time = p_time
                stoptime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(p_time),
                                                                                                        '%Y-%m-%d %H:%M:%S')
            m, s = divmod(stoptime_diff.total_seconds(), 60)
            h, m = divmod(m, 60)
            dur_h = (_('%0*d') % (2, h))
            dur_m = (_('%0*d') % (2, m * 1.677966102))
            duration = dur_h + '.' + dur_m
            data = {'name': self.description,
                    'date': datetime.now(),
                    'start_date': start_time if project_task else '',
                    'project_id': project_task.project_id.id,
                    'task_id': project_task.id,
                    'unit_amount': float(duration),
                    'user_id': self._uid}
            data_list.append((0, 0, data))
            project_task.write({'state': 'stop', 'timesheet_ids': data_list})
        return True