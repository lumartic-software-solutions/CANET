from odoo import models, fields, api, _


class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    maintenance_id = fields.Many2one('maintenance.request','Maintenanance')
    time = fields.Char('Maintenance Time')

class Maintenanace(models.Model):
    _inherit = 'maintenance.request'

    reference = fields.Char('Reference', readonly=True)
    start_datetime = fields.Datetime('Start Process Datetime')
    end_datetime = fields.Datetime('Stop Process Datetime')
    user_ids = fields.Many2many('res.users', 'req_id', 'user_id', 'maintenance_user_rel', 'Responsible')
    operations = fields.One2many(
        'maintenance.request.line', 'maintenance_id', 'Parts',
        copy=True)
    timesheet_ids = fields.One2many('account.analytic.line', 'maintenance_id', 'Time Parts')
    amount_untaxed = fields.Float('Untaxed Amount', compute='_amount_untaxed', store=True)
    amount_tax = fields.Float('Taxes', compute='_amount_tax', store=True)
    amount_total = fields.Float('Total', compute='_amount_total', store=True)
    state = fields.Selection([('draft','New Request'),('in_process','In Process'),('end','End'),('cancel','Cancel')], string='State',readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    @api.one
    @api.depends('operations.price_subtotal')
    def _amount_untaxed(self):
        total = sum(operation.price_subtotal for operation in self.operations)
        self.amount_untaxed = total

    @api.one
    @api.depends('operations.price_unit', 'operations.product_uom_qty', 'operations.product_id',)
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
    @api.depends('price_unit', 'maintenance_id', 'product_uom_qty', 'product_id','tax_id')
    def _compute_price_subtotal(self):
        taxes = self.tax_id.compute_all(self.price_unit, self.env.user.currency_id, self.product_uom_qty,
                                        self.product_id, self.env.user.partner_id)
        self.price_subtotal = taxes['total_excluded']
