from odoo import models, fields, api, tools, _
import datetime
from odoo.tools import float_compare, pycompat


class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    maintenance_id = fields.Many2one('maintenance.request', 'Maintenanance')
    time = fields.Char('Maintenance Time')
    start_date = fields.Datetime(string="Start Date")
    date = fields.Datetime('End Date', required=True, index=True, default=datetime.datetime.now())


class Maintenanace(models.Model):
    _inherit = 'maintenance.request'

    reference = fields.Char('Reference', readonly=True)
    start_date = fields.Date(string="Start Date")
    start_time = fields.Datetime("Start Time")
    con_time = fields.Datetime("Continue Time")
    end_time = fields.Datetime("End Time")
    restart_time = fields.Datetime("Restart Time")
    user_ids = fields.Many2many('res.users', 'req_id', 'user_id', 'maintenance_user_rel', 'Responsible')
    operations = fields.One2many(
        'maintenance.request.line', 'maintenance_id', 'Parts',
        copy=True)
    timesheet_ids = fields.One2many('account.analytic.line', 'maintenance_id', 'Time Parts')
    amount_untaxed = fields.Float('Untaxed Amount', compute='_amount_untaxed', store=True)
    amount_tax = fields.Float('Taxes', compute='_amount_tax', store=True)
    amount_total = fields.Float('Total', compute='_amount_total', store=True)
    state = fields.Selection(
        [('draft', 'New'), ('start', 'Start'), ('continue', 'Continue'), ('stop', 'Stop'), ('end', 'End')],
        string='Status', default='draft')
    equipment_ids = fields.One2many('maintenance.equipment.task', 'maintenance_id', 'Equipments')

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
    def archive_equipment_request(self):
        self.write({'state': 'cancel'})

    @api.model
    def create(self, vals):
        vals['reference'] = self.env['ir.sequence'].next_by_code('maintenance.req') or _('New')
        result = super(Maintenanace, self).create(vals)
        return result

    @api.depends('reference')
    def name_get(self):
        result = []
        reference = ''
        for line in self:
            if line.reference:
                reference = line.reference
            result.append((line.id, reference))
        return result


class MaintenanaceRequestLine(models.Model):
    _name = 'maintenance.request.line'
    _description = 'Maintenance Line'

    name = fields.Char('Description', required=True)
    maintenance_id = fields.Many2one(
        'maintenance.request', 'maintenance request Reference',
        index=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    invoiced = fields.Boolean('Invoiced', copy=False, readonly=True)
    price_unit = fields.Float('Unit Price', required=True)
    price_subtotal = fields.Float('Subtotal', compute='_compute_price_subtotal', digits=0)
    tax_id = fields.Many2many(
        'account.tax', 'maintenanace_line_rel', 'maintenanace_operation_line_id', 'tax_id', 'Taxes')
    product_uom_qty = fields.Float(
        'Quantity', default=1.0, required=True)
    product_uom = fields.Many2one(
        'product.uom', 'Product Unit of Measure',
        required=True)
    invoice_line_id = fields.Many2one(
        'account.invoice.line', 'Invoice Line',
        copy=False, readonly=True)
    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        index=True, required=True)
    location_dest_id = fields.Many2one(
        'stock.location', 'Dest. Location',
        index=True, required=True)
    move_id = fields.Many2one(
        'stock.move', 'Inventory Move',
        copy=False, readonly=True)
    lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial')

    '''@api.onchange('type', 'maintenance_id')
    def onchange_operation_type(self):
        if not self.type:
            self.location_id = False
            self.location_dest_id = False
        elif self.type == 'add':
            self.onchange_product_id()
            args = self.maintenance_id.company_id and [('company_id', '=', self.maintenance_id.company_id.id)] or []
            warehouse = self.env['stock.warehouse'].search(args, limit=1)
            self.location_id = warehouse.lot_stock_id
            self.location_dest_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id
        else:
            self.price_unit = 0.0
            self.tax_id = False
            self.location_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id
            self.location_dest_id = self.env['stock.location'].search([('scrap_location', '=', True)], limit=1).id'''

    @api.onchange('maintenance_id', 'product_id', 'product_uom_qty')
    def onchange_product_id(self):
        if not self.product_id or not self.product_uom_qty:
            return
        if self.product_id:
            self.name = self.product_id.display_name
            self.product_uom = self.product_id.uom_id.id
            self.tax_id = self.product_id.taxes_id
            self.price_unit = self.product_id.list_price

    @api.one
    @api.depends('price_unit', 'maintenance_id', 'product_uom_qty', 'product_id', 'tax_id')
    def _compute_price_subtotal(self):
        taxes = self.tax_id.compute_all(self.price_unit, self.env.user.currency_id, self.product_uom_qty,
                                        self.product_id, self.env.user.partner_id)
        self.price_subtotal = taxes['total_excluded']


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    state = fields.Selection([('in_stock','In Stock'),('delivery','Delivery'),('return','Return')],'State',default='in_stock')

    image_variant = fields.Binary(
        "Variant Image", attachment=True,
    )
    image = fields.Binary(
        "Big-sized image", compute='_compute_images', inverse='_set_image',
    )
    image_small = fields.Binary(
        "Small-sized image", compute='_compute_images', inverse='_set_image_small',
    )
    image_medium = fields.Binary(
        "Medium-sized image", compute='_compute_images', inverse='_set_image_medium',
    )
    default_code = fields.Char('Internal Reference')

    barcode = fields.Char('Barcode')
    task_count = fields.Integer(string="Task", compute='_compute_task_count')
    count_maintenance = fields.Integer(string="Maintenance", compute='_compute_maintenance')
    equipment_ids = fields.One2many('maintenance.equipment.task', 'equipment_id', 'History')

    @api.multi
    def _compute_task_count(self):
        task_data = self.env['maintenance.equipment.task'].search([('equipment_id', '=', self.id)])
        count = 0
        if task_data:
            for task in task_data:
                if task.task_id:
                    count += 1
        if count:
            self.task_count = count

    @api.multi
    def _compute_maintenance(self):
        maintenance_data = self.env['maintenance.equipment.task'].search([('equipment_id', '=', self.id)])
        count = 0
        if maintenance_data:
            for maintenance in maintenance_data:
                if maintenance.maintenance_id:
                    count += 1
        if count:
            self.count_maintenance = count

    def action_equipment_task(self):
        action = self.env.ref('canet_maintenance.action_view_task_canet').read()[0]
        task_ids = []
        task_data = self.env['maintenance.equipment.task'].search([('equipment_id', '=', self.id)])
        if task_data:
            for task in task_data:
                if task.task_id:
                    task_ids.append(task.task_id.id)
        action['res_ids'] = task_ids
        return action

    def action_equipment_maintenance(self):
        action = self.env.ref('canet_maintenance.action_view_maintenance_canet').read()[0]
        maintenance_ids = []
        maintenance_data = self.env['maintenance.equipment.task'].search([('equipment_id', '=', self.id)])
        if maintenance_data:
            for maintenance in maintenance_data:
                if maintenance.maintenance_id:
                    maintenance_ids.append(maintenance.maintenance_id.id)
        action['res_ids'] = maintenance_ids
        return action

    @api.one
    def _compute_images(self):
        if self._context.get('bin_size'):
            self.image_medium = self.image_variant
            self.image_small = self.image_variant
            self.image = self.image_variant
        else:
            resized_images = tools.image_get_resized_images(self.image_variant, return_big=True,
                                                            avoid_resize_medium=True)
            self.image_medium = resized_images['image_medium']
            self.image_small = resized_images['image_small']
            self.image = resized_images['image']

    @api.one
    def _set_image(self):
        self._set_image_value(self.image)

    @api.one
    def _set_image_medium(self):
        self._set_image_value(self.image_medium)

    @api.one
    def _set_image_small(self):
        self._set_image_value(self.image_small)

    @api.one
    def _set_image_value(self, value):
        if isinstance(value, pycompat.text_type):
            value = value.encode('ascii')
        image = tools.image_resize_image_big(value)
        self.image_variant = image


class MaintenanceEquipmentTask(models.Model):
    _name = 'maintenance.equipment.task'

    task_id = fields.Many2one('project.task', 'Task')
    user_id = fields.Many2one('res.users', 'Employee')
    description = fields.Char('Description')
    equipment_id = fields.Many2one('maintenance.equipment', 'Equipments')
    units = fields.Float('Units')
    barcode = fields.Char('Barcode')
    date_in = fields.Date('Date In')
    date_out = fields.Date('Date Out')
    state = fields.Selection([('delivery', 'Delivery'), ('return', 'Return')], 'State')
    maintenance_id = fields.Many2one('maintenance.request', 'Maintenance')

    @api.onchange('equipment_id')
    def onchange_equipment_id(self):
        if self.equipment_id:
            self.description = self.equipment_id.note or ''
            self.barcode = self.equipment_id.barcode
