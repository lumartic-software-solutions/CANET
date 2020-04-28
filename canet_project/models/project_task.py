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
    operations = fields.One2many(
        'maintenance.request.line', 'task_id', 'Parts',
        copy=True)
    amount_untaxed = fields.Float('Untaxed Amount', compute='_amount_untaxed', store=True)
    amount_tax = fields.Float('Taxes', compute='_amount_tax', store=True)
    amount_total = fields.Float('Total', compute='_amount_total', store=True)
    state = fields.Selection(
        [('draft', 'New'), ('start', 'Start'), ('continue', 'Continue'), ('end', 'End'), ('stop', 'Stop')],
        string='Status', default='draft')

    @api.one
    @api.depends('operations.price_subtotal')
    def _amount_untaxed(self):
        total = sum(operation.price_subtotal for operation in self.operations)
        self.amount_untaxed = total

    @api.one
    @api.depends('operations.price_unit', 'operations.product_uom_qty', 'operations.product_id', )
    def _amount_tax(self):
        val = 0.0
        for operation in self.operations:
            if operation.tax_id:
                tax_calculate = operation.tax_id.compute_all(operation.price_unit, self.env.user.currency_id,
                                                             operation.product_uom_qty, operation.product_id,
                                                             self.env.user.partner_id)
                for c in tax_calculate['taxes']:
                    val += c['amount']
        self.amount_tax = val

    @api.one
    @api.depends('amount_untaxed', 'amount_tax')
    def _amount_total(self):
        self.amount_total = (self.amount_untaxed + self.amount_tax)


    @api.multi
    def stop_task(self):
        context = self._context
        if context.get('stop_task'):
            for i in self:
                i.write({'state': 'stop'})


class MaintenanaceRequestLine(models.Model):
    _inherit = 'maintenance.request.line'

    fields.Char('Description', required=True)
    task_id = fields.Many2one(
        'project.task', 'Proect Task Reference',
        index=True, ondelete='cascade')


