# -*- coding: utf-8 -*-
# Odoo, Open Source Ballesater Screen.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).# 

from odoo import fields, models, api, _
from odoo.exceptions import UserError
    
# new fields 
class StockInventory(models.Model):
    _inherit = 'stock.inventory'
     
    user_id = fields.Many2one('res.users', 'Responsible')
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
        result = super(StockInventory, self).create(vals)
        return result
    
    
    # write the product in lot id
    def action_done(self):
        sample_product_id = self.env.ref('ballester_screen.sample_product_id').id
        for line in self.line_ids :
            if line.prod_lot_id :
                if line.prod_lot_id.product_id.id == sample_product_id :
                    line.prod_lot_id.write({'product_id' : line.product_id.id})
        negative = next((line for line in self.mapped('line_ids') if line.product_qty < 0 and line.product_qty != line.theoretical_qty), False)
        if negative:
            raise UserError(_('You cannot set a negative product quantity in an inventory line:\n\t%s - qty: %s') % (negative.product_id.name, negative.product_qty))
        self.action_check()
        self.write({'state': 'done'})
        self.post_inventory()
        
        return True
    
    
# change prod_lot_id domain     
class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    sample_product_id = fields.Many2one(
        'product.product', 'Sample_product'
        )
    prod_lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number'
        )
    
    # set the sample product
    @api.model
    def default_get(self, vals):
        res = super(InventoryLine, self).default_get(vals)
        ctx = dict(self._context)
        if 'default_filter' in ctx :
            if ctx.get('default_filter') == 'none' :
                res.update({'sample_product_id': self.env.ref('ballester_screen.sample_product_id').id})
        return res
