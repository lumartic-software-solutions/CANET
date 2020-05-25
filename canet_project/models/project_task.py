from odoo import models, fields, api, _
import datetime


class ProjectTask(models.Model):
    _inherit = 'project.task'
    start_date = fields.Date(string="Start Date")
    start_time = fields.Datetime("Start Time")
    con_time = fields.Datetime("Continue Time")
    end_time = fields.Datetime("End Time")
    number = fields.Char('Number')
    restart_time = fields.Datetime("Restart Time")
    operations = fields.One2many(
        'maintenance.request.line', 'task_id', 'Parts',
        copy=True)
    amount_untaxed = fields.Float('Untaxed Amount', compute='_amount_untaxed', store=True)
    amount_tax = fields.Float('Taxes', compute='_amount_tax', store=True)
    amount_total = fields.Float('Total', compute='_amount_total', store=True)
    state = fields.Selection(
        [('draft', 'New'), ('start', 'Start'), ('continue', 'Continue'), ('stop', 'Stop'), ('end', 'End')],
        string='Status', default='draft')
    # user_ids = fields.Many2many('res.users','task_id','user_id','task_user_rel','Employees')
    equipment_ids = fields.One2many('maintenance.equipment.task', 'task_id', 'Equipments')

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

    @api.model
    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].next_by_code('project.task') or _('New')
        result = super(ProjectTask, self).create(vals)
        return result

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


class MaintenanceEquipmentTask(models.Model):
    _name = 'maintenance.equipment.task'

    task_id = fields.Many2one('project.task','Task')
    user_id = fields.Many2one('res.users','Employee')
    description = fields.Char('Description')
    equipment_id = fields.Many2one('maintenance.equipment','Equipments')
    units = fields.Float('Units')
    barcode = fields.Char('Barcode')
    date_in = fields.Date('Date In')
    date_out = fields.Date('Date Out')
    state= fields.Selection([('delivery','Delivery'),('return','Return')], 'State')

    @api.onchange('equipment_id')
    def onchange_equipment_id(self):
        if self.equipment_id:
            self.description = self.equipment_id.note or ''
            self.barcode =  self.equipment_id.barcode
