from odoo import models, fields, api, _
import datetime


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    start_date = fields.Datetime(string="Start Date")
    date = fields.Datetime('End Date', required=True, index=True, default=datetime.datetime.now())


class ProjectTask(models.Model):
    _inherit = 'project.task'
    start_date = fields.Date(string="Start Date")
    start_time = fields.Datetime("Start Time")
    con_time = fields.Datetime("Continue Time")
    end_time = fields.Datetime("End Time")
    restart_time = fields.Datetime("Restart Time")
    state = fields.Selection(
        [('draft', 'New'), ('start', 'Start'), ('continue', 'Continue'), ('end', 'End'), ('stop', 'Stop')],
        string='Status', default='draft')

    @api.multi
    def stop_task(self):
        context = self._context
        if context.get('stop_task'):
            for i in self:
                i.write({'state': 'stop'})