# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    wash_id = fields.Many2one('wash.order','Wash Order') 



class WashOrder(models.Model):
    _name = 'wash.order'
   
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    @api.model
    def _default_stock_location(self):
        warehouse = self.env['stock.warehouse'].search([], limit=1)
        if warehouse:
            return warehouse.lot_stock_id.id
        return False


    name = fields.Char(
        'Wash Reference',
        copy=False, required=True,
      readonly=True, 
	default=lambda self: _('New'),)
    wash_date = fields.Datetime('Date', default=fields.Datetime.now())
    end_wash_datetime = fields.Datetime('Process End Time')
    product_id = fields.Many2one(
        'product.product', string='Product to Wash',
        readonly=True, required=True, states={'draft': [('readonly', False)]})
    recycled_product_id = fields.Many2one(
        'product.product', string='Recycled Product',
        readonly=True,  states={'draft': [('readonly', False)]})
    product_qty = fields.Float(
        'Product Quantity',
        default=1.0, digits=dp.get_precision('Product Unit of Measure'),
        readonly=True, required=True, states={'draft': [('readonly', False)]})
    product_uom = fields.Many2one(
        'product.uom', 'Product Unit of Measure',
        readonly=True, required=True, states={'draft': [('readonly', False)]})
    partner_id = fields.Many2one(
        'res.partner', 'Customer',
        index=True, states={'start_ash': [('readonly', True)]},
        help='Choose partner for whom the order will be invoiced and delivered.')
    address_id = fields.Many2one(
        'res.partner', 'Delivery Address',
        domain="[('parent_id','=',partner_id)]",
        states={'start_wash': [('readonly', True)]})
    default_address_id = fields.Many2one('res.partner', compute='_compute_default_address_id')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('cancel', 'Cancelled'),
        ('start_emptying', 'Start Emptying'),
        ('stop_emptying', 'Stop  Emptying'),
        ('start_re_wash', 'Start Pre-wash'),
        ('stop_re_wash', 'Stop  Pre-wash'),
        ('start_wash', 'Start Wash'),
        ('end_wash', 'End wash'),
        ('start_drying', 'Start Drying'),
        ('stop_drying', 'Stop Drying'),
	('start_crush', 'Start Crush/Compact'),
	('stop_crush', 'End Crush/Compact'),
	('check_compliance', 'Compliance Checked'),
	('quality_control', 'Quality Control'),
	('repair_create','Repair Created'),
	#('convert','Convert Recycled Product'),
	('destructed','Destructed'),
        ('transfer_to_store', 'Transfer To Store'),], string='Status',
        copy=False, default='draft', readonly=True, track_visibility='onchange')
    location_id = fields.Many2one(
        'stock.location', 'Current Location',
        index=True, readonly=True, required=True,
        states={'draft': [('readonly', False)], 'start_wash': [('readonly', True)]})
    location_dest_id = fields.Many2one(
        'stock.location', 'Delivery Location',
        readonly=True, required=True,
        states={'draft': [('readonly', False)], 'start_wash': [('readonly', True)]})
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial',
        domain="[('product_id','=', product_id)]",
        help="Products repaired are all belonging to this lot", oldname="prodlot_id")
    lot_name = fields.Char('Lot Number',related="lot_id.name")
    guarantee_limit = fields.Date('Warranty Expiration', states={'start_wash': [('readonly', True)]})
    operations = fields.One2many(
        'wash.order.line', 'wash_id', 'Parts',
        copy=True, readonly=True, states={'draft': [('readonly', False)]})
    pricelist_id = fields.Many2one(
        'product.pricelist', 'Pricelist',
        default=lambda self: self.env['product.pricelist'].search([], limit=1).id,
        help='Pricelist of the selected partner.')
    partner_invoice_id = fields.Many2one('res.partner', 'Invoicing Address')
    ''''invoice_method = fields.Selection([
        ("none", "No Invoice"),
        ("b4repair", "Before Repair"),
        ("after_repair", "After Repair")], string="Invoice Method",
        default='none', index=True, readonly=True, required=True,
        states={'draft': [('readonly', False)]},
        help='Selecting \'Before Repair\' or \'After Repair\' will allow you to generate invoice before or after the repair is done respectively. \'No invoice\' means you don\'t want to generate invoice for this repair order.')
    invoice_id = fields.Many2one(
        'account.invoice', 'Invoice',
        copy=False, readonly=True, track_visibility="onchange")
    move_id = fields.Many2one(
        'stock.move', 'Move',
        copy=False, readonly=True, track_visibility="onchange",
        help="Move created by the repair order")'''
    internal_notes = fields.Text('Internal Notes',readonly=True)
    quotation_notes = fields.Text('Quotation Notes')
    company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env['res.company']._company_default_get('mrp.repair'))
    invoiced = fields.Boolean('Invoiced', copy=False, readonly=True)
    repaired = fields.Boolean('Repaired', copy=False, readonly=True)
    repair_compliance = fields.Selection([('yes','yes'),('no','no')],'REpair Compliance Answer')
    amount_untaxed = fields.Float('Untaxed Amount', compute='_amount_untaxed', store=True)
    amount_tax = fields.Float('Taxes', compute='_amount_tax', store=True)
    amount_total = fields.Float('Total', compute='_amount_total', store=True)
    tracking = fields.Selection('Product Tracking', related="product_id.tracking")
    inventory_ids = fields.One2many('stock.inventory','wash_id','Recycled Product')
    washing_type= fields.Selection([('dangerous','Dangerous'),('non_dangerous','Non-Dangerous')],'Washing Type')
    dangerous = fields.Boolean('Dangerous')
    non_dangerous = fields.Boolean('Non-Dangerous')
    timesheet_ids = fields.One2many('account.analytic.line','wash_id', 'Time Parts')
    type_of_order = fields.Selection([('container','Wash Container'),('drum','Wash Drums'),('crush','Crushing'),('compact','Compression')],'Type Of Order')
    type_of_drum = fields.Selection([('plastic','Plastic Drum'),('metal','Metal Drums')], 'Type Of Drum',related="product_id.type_of_drum")
    start_datetime= fields.Datetime('Start Wash Datetime')
    wash_id = fields.Many2one('wash.order',readonly="True")
    cage = fields.Boolean('Cage',related ="recycled_product_id.cage",store=True)
    crush_qty = fields.Float('Crush/Compact material Quantity')
	
    '''_sql_constraints = [
        ('lot_id_uniq', 'unique(lot_id)', 'Lot number already use in another Wash order!'),
    ] '''   


    @api.onchange('washing_type')
    def _onchange_washing_type(self):
        dangerous_obj = self.env['dangerous.product']
        args = self.company_id and [('company_id', '=', self.company_id.id)] or []
        warehouse = self.env['stock.warehouse'].search(args, limit=1)
        if self.washing_type == 'dangerous':
            self.dangerous = True
            self.non_dangerous = False
     
            dangerous_product_con_ids =dangerous_obj.search([('type_product','=','container'),('dangerous','=', True)])
            dangerous_product_drum_ids = dangerous_obj.search([('type_product','=','drum'),('dangerous','=', True)])
            if  dangerous_product_con_ids:
               if self.type_of_order == 'container':
                   wash_line = []
                   for product  in dangerous_product_con_ids:
                       vals = {
                               'product_id': product.product_id.product_variant_id.id,
                                'type':'add',
                                'name':product.product_id.display_name,
                                'product_uom_qty':product.qty,
                                'product_uom': product.product_id.uom_id.id,
				'location_dest_id': self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id,
				'location_id': warehouse.lot_stock_id,
                                  }
                       wash_line.append((0,0,vals))
                   self.operations = wash_line
            if dangerous_product_drum_ids:
               if self.type_of_order == 'drum':
                   wash_line = []
                   for product  in dangerous_product_drum_ids:
                       vals = {
                               'product_id':product.product_id.product_variant_id.id,
                                'type':'add',
                                'name':product.product_id.display_name,
                                'product_uom_qty':product.qty,
                                'product_uom': product.product_id.uom_id.id,
				'location_dest_id': self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id,
				'location_id': warehouse.lot_stock_id,
                                  }

                       wash_line.append((0,0,vals))
                   self.operations = wash_line
        elif self.washing_type == 'non_dangerous':
            self.non_dangerous = True
            self.dangerous = False
            nondangerous_product_con_ids =dangerous_obj.search([('type_product','=','container'),('non_dangerous','=', True)])
            nondangerous_product_drum_ids = dangerous_obj.search([('type_product','=','drum'),('non_dangerous','=', True)])
            if  nondangerous_product_con_ids:
               if self.type_of_order == 'container':
                   wash_line = []
                   for product  in nondangerous_product_con_ids:
                       vals = {
                               'product_id': product.product_id.product_variant_id.id,
                                'type':'add',
                                'name':product.product_id.display_name,
                                'product_uom_qty':product.qty,
                                'product_uom': product.product_id.uom_id.id,
				'location_dest_id': self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id,
				'location_id': warehouse.lot_stock_id,
                                  }
                       wash_line.append((0,0,vals))
                   self.operations = wash_line
            if nondangerous_product_drum_ids:
               if self.type_of_order == 'drum':
                   wash_line = []
                   for product  in nondangerous_product_drum_ids:
                       vals = {
                               'product_id':product.product_id.product_variant_id.id,
                                'type':'add',
                                'name':product.product_id.display_name,
                                'product_uom_qty':product.qty,
                                'product_uom': product.product_id.uom_id.id,
				'location_dest_id': self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id,
				'location_id': warehouse.lot_stock_id,
                                  }
                       wash_line.append((0,0,vals))
                   self.operations = wash_line
    
    @api.one
    @api.depends('operations.price_subtotal', 'pricelist_id.currency_id')
    def _amount_untaxed(self):
        total = sum(operation.price_subtotal for operation in self.operations)
        self.amount_untaxed = self.pricelist_id.currency_id.round(total)

    @api.one
    @api.depends('operations.price_unit', 'operations.product_uom_qty', 'operations.product_id',
                 'pricelist_id.currency_id', 'partner_id')
    def _amount_tax(self):
        val = 0.0
        for operation in self.operations:
            if operation.tax_id:
                tax_calculate = operation.tax_id.compute_all(operation.price_unit, self.pricelist_id.currency_id, operation.product_uom_qty, operation.product_id, self.partner_id)
                for c in tax_calculate['taxes']:
                    val += c['amount']
        self.amount_tax = val
		
    @api.onchange('product_uom')
    def onchange_product_uom(self):
        res = {}
        if not self.product_id or not self.product_uom:
            return res
        if self.product_uom.category_id != self.product_id.uom_id.category_id:
            res['warning'] = {'title': _('Warning'), 'message': _('The Product Unit of Measure you chose has a different category than in the product form.')}
            self.product_uom = self.product_id.uom_id.id
        return res

    
    @api.onchange('product_qty', 'product_uom')
    def _onchange_product_id_check_availability(self):
        if not self.product_id or not self.product_qty or not self.product_uom:
            self.product_packaging = False
            return {}
        warehouse_id = False
        if not self.location_id:
            raise UserError(_("Please first select location"))
        if self.product_id.type == 'product':
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            location_name= self.location_id.location_id.name
            warehouse_id =self.env['stock.warehouse'].search([('code','=', location_name)])
            product = self.product_id.with_context(
              
            )
            product_qty = self.product_uom._compute_quantity(self.product_qty, self.product_id.uom_id)
            if float_compare(product.virtual_available, product_qty, precision_digits=precision) == -1:
                message =  _('You plan to sell %s %s but you only have %s %s available in %s warehouse.') % \
                        (self.product_qty, self.product_uom.name, product.virtual_available, product.uom_id.name, warehouse_id[0].name)
                # We check if some products are available in other warehouses.
                if float_compare(product.virtual_available, self.product_id.virtual_available, precision_digits=precision) == -1:
                    message += _('\nThere are %s %s available accross all warehouses.') % \
                            (self.product_id.virtual_available, product.uom_id.name)

                warning_mess = {
                    'title': _('Not enough inventory!'),
                    'message' : message
                }
                return {'warning': warning_mess}
        return {}
    
    
    @api.multi
    def action_view_repair(self):
        action = self.env.ref('mrp_repair.action_repair_order_tree')
        result = action.read()[0]
        repair_obj =self.env['mrp.repair'].search([('wash_id','=',self.id)])
        if not repair_obj:
           raise UserError(_("There is no record of Repair"))
        result['context'] = {'default_wash_order_id': self.id,'default_search_wash_order_id':self.id}
        res = self.env.ref('mrp_repair.view_repair_order_form', False)
        result['views'] = [(res and res.id or False, 'form')]
        result['res_id'] = repair_obj[0].id
        return result


    @api.multi
    def action_view_crush(self):
        action = self.env.ref('ballester_wash.action_wash_order_tree_crush')
        result = action.read()[0]
        wash_search_ids =self.env['wash.order'].search([('wash_id','=',self.id),('type_of_order','=','crush')])
        if not wash_search_ids:
            raise UserError(_("There is no record of Crush")) 
        res = self.env.ref('ballester_wash.view_wash_order_crush_form', False)
        result['views'] = [(res and res.id or False, 'form')]
        result['res_id'] = wash_search_ids[0].id
        return result


    @api.multi
    def action_view_compact(self):
        action = self.env.ref('ballester_wash.action_wash_order_tree_compact')
        result = action.read()[0]
        wash_search_ids =self.env['wash.order'].search([('wash_id','=',self.id),('type_of_order','=','compact')])
        if not wash_search_ids:
            raise UserError(_("There is no record of Compact"))
        res = self.env.ref('ballester_wash.view_wash_order_crush_form', False)
        result['views'] = [(res and res.id or False, 'form')]
        result['res_id'] = wash_search_ids[0].id
        return result


    @api.one
    @api.depends('amount_untaxed', 'amount_tax')
    def _amount_total(self):
        self.amount_total = self.pricelist_id.currency_id.round(self.amount_untaxed + self.amount_tax)

    @api.one
    @api.depends('partner_id')
    def _compute_default_address_id(self):
        if self.partner_id:
            self.default_address_id = self.partner_id.address_get(['contact'])['contact']
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        self.guarantee_limit = False
        self.lot_id = False
        if self.product_id:
            self.product_uom = self.product_id.uom_id.id
            self.product_qty = 1.0
            if self.product_id.recycled_product_id:
                self.recycled_product_id = self.product_id.recycled_product_id.id

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if not self.partner_id:
            self.address_id = False
            self.partner_invoice_id = False
            self.pricelist_id = self.env['product.pricelist'].search([], limit=1).id
        else:
            addresses = self.partner_id.address_get(['delivery', 'invoice', 'contact'])
            self.address_id = addresses['delivery'] or addresses['contact']
            self.partner_invoice_id = addresses['invoice']
            self.pricelist_id = self.partner_id.property_product_pricelist.id


    @api.model
    def create(self, vals):
        context = self._context
        if vals.get('name', _('New')) == _('New') and context.get('default_type_of_order') == 'container':
            vals['name'] = self.env['ir.sequence'].next_by_code('wash.order.container') or _('New')
        if vals.get('name', _('New')) == _('New') and context.get('default_type_of_order') == 'drum':
            vals['name'] = self.env['ir.sequence'].next_by_code('wash.order.drum') or _('New')
        if vals.get('name', _('New')) == _('New') and context.get('default_type_of_order') == 'crush':
            vals['name'] = self.env['ir.sequence'].next_by_code('wash.order.crush') or _('New')
        if vals.get('name', _('New')) == _('New') and context.get('default_type_of_order') == 'compact':
            vals['name'] = self.env['ir.sequence'].next_by_code('wash.order.compact') or _('New')
        result = super(WashOrder,self).create(vals)
        return result

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        context = self._context or {}
        return super(WashOrder, self).search(args, offset, limit, order, count=count)
    
    @api.multi
    def action_wash_cancel_draft(self):
        if self.filtered(lambda wash: wash.state != 'cancel'):
            raise UserError(_("Wash must be canceled in order to reset it to draft."))
        self.mapped('operations').write({'state': 'draft'})
        return self.write({'state': 'draft'})

    @api.multi
    def action_wash_cancel(self):
        if self.filtered(lambda repair: repair.state == 'transfer_to_store'):
            raise UserError(_("Cannot cancel completed Wash order."))
        self.mapped('operations').write({'state': 'cancel'})
        return self.write({'state': 'cancel'})


    '''@api.multi
    def action_transfer_to_store(self):
        inventory_obj = self.env['stock.inventory']
        if self.recycled_product_id:
            pro_line_values = {  
                            'product_id' :self.product_id.id,
                            'product_uom_id' :self.product_id.uom_id.id,
                            'prod_lot_id' :self.lot_id.id,
                            'product_qty' :0,
                            'location_id' :self.location_id.id,
                            'state':'confirm'
                            }
            pro_inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
            pro_inv_vals = {'name' :pro_inventory_sequence,
                   'filter':'product',
                   'line_ids': [(0, 0,  pro_line_values)],
                   'location_id' :self.location_id.id,
                   'product_id': self.product_id.id,
                   'wash_id': self.id
                    }
            pro_inv = inventory_obj.create(pro_inv_vals)
            pro_inv.action_start()
            pro_inv.action_done()
            ###recycled product inventory
            line_values = {  
                            'product_id' :self.recycled_product_id.id,
                            'product_uom_id' :self.recycled_product_id.uom_id.id,
                            'prod_lot_id' :self.lot_id.id,
                            'product_qty' : 1,
                            'location_id' :self.location_id.id,
                            'state':'confirm'
                            }
            inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
            inv_vals = {'name' :inventory_sequence,
                   'filter':'product',
                   'line_ids': [(0, 0,  line_values)],
                   'location_id' :self.location_id.id,
                   'product_id': self.recycled_product_id.id,
                   'wash_id': self.id
                    }
            pro_inv = inventory_obj.create(inv_vals)
            pro_inv.action_start()
            pro_inv.action_done()
            lot_search = self.env['stock.production.lot'].search([('name','=',self.lot_id.name)])
            if lot_search:
                lot_search.with_context(wash_lot=True).write({'product_id':self.recycled_product_id.id })
            return self.write({'state': 'transfer_to_store'})'''
        
    
    '''@api.multi
    def action_destruction_wash(self):
        return self.write({'state': 'destructed'})'''

    @api.multi
    def action_wash_start_crush(self):
        return self.write({'state': 'start_crush'})

    @api.multi
    def action_wash_stop_crush(self):
        return self.write({'state': 'stop_crush'})


class WashOrderLine(models.Model):
    _name = 'wash.order.line'
    _description = 'Wash Line'

    name = fields.Char('Description', required=True)
    wash_id = fields.Many2one(
        'wash.order', 'Wash Order Reference',
        index=True, ondelete='cascade')
    type = fields.Selection([
        ('add', 'Add'),
        ('remove', 'Remove')], 'Type', required=True)
    product_id = fields.Many2one('product.product', 'Product To Wash', required=True)
    washing_type= fields.Selection('Washing Type',related='wash_id.washing_type')
    invoiced = fields.Boolean('Invoiced', copy=False, readonly=True)
    price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'))
    price_subtotal = fields.Float('Subtotal', compute='_compute_price_subtotal', digits=0)
    tax_id = fields.Many2many(
        'account.tax', 'wash_operation_line_tax', 'wash_operation_line_id', 'tax_id', 'Taxes')
    product_uom_qty = fields.Float(
        'Quantity', default=1.0,
        digits=dp.get_precision('Product Unit of Measure'), required=True)
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
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancelled')], 'Status', default='draft',
        copy=False, readonly=True, required=True,
        help='The status of a repair line is set automatically to the one of the linked repair order.')


    @api.onchange('type', 'wash_id')
    def onchange_operation_type(self):
        if not self.type:
            self.location_id = False
            self.location_dest_id = False
        elif self.type == 'add':
            self.onchange_product_id()
            args = self.wash_id.company_id and [('company_id', '=', self.wash_id.company_id.id)] or []
            warehouse = self.env['stock.warehouse'].search(args, limit=1)
            self.location_id = warehouse.lot_stock_id
            self.location_dest_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id
        else:
            self.price_unit = 0.0
            self.tax_id = False
            self.location_id = self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id
            self.location_dest_id = self.env['stock.location'].search([('scrap_location', '=', True)], limit=1).id 

    @api.onchange('wash_id', 'product_id', 'product_uom_qty')
    def onchange_product_id(self):
        partner = self.wash_id.partner_id
        if not self.product_id or not self.product_uom_qty:
            return
        if self.product_id:
            if partner:
                self.name = self.product_id.with_context(lang=partner.lang).display_name
            else:
                self.name = self.product_id.display_name
            self.product_uom = self.product_id.uom_id.id
        if self.type != 'remove':
            if partner and self.product_id:
                self.tax_id = partner.property_account_position_id.map_tax(self.product_id.taxes_id, self.product_id, partner).ids


    @api.one
    @api.depends('price_unit', 'wash_id', 'product_uom_qty', 'product_id')
    def _compute_price_subtotal(self):
        taxes = self.tax_id.compute_all(self.price_unit, self.wash_id.pricelist_id.currency_id, self.product_uom_qty, self.product_id, self.wash_id.partner_id)
        self.price_subtotal = taxes['total_excluded']
      

