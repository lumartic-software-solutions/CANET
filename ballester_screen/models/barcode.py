# -*- coding: utf-8 -*-
# Odoo, Open Source Ballesater Screen.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).# 

import odoo
from odoo import fields, models,api,_


# class GenerateBarcode(models.Model):
#     _name = 'generate.barcode'
# 
#     barcode = fields.Char('Barcode')
#     status = fields.Selection([('new', 'New'),
#                                ('used', 'Used'),
#                                ],
#                               'Status')
    
# class LotAttributeLine(models.Model):
#     _inherit = "lot.attribute.line"
#     
#     lot_id = fields.Many2one('stock.production.lot','Lot')
     
#     # set the product_tmpl_id and lot_id
#     @api.model
#     def default_get(self, vals):
#         res = super(LotAttributeLine, self).default_get(vals)
#         context = self._context
#         if 'lot_id'  in context  and  context.get('lot_id') != None :
#             lot_id = self.env['stock.production.lot'].browse(int(context.get('lot_id')))
#             if lot_id :
#                 res.update({'lot_id':lot_id.id})
#         return res
    
    
#new fields 
class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
     
    is_created = fields.Boolean('Is Created Lot details ?',default=False)
