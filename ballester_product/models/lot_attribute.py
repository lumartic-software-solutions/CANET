# -*- coding: utf-8 -*-
# Odoo, Open Source Ballester Product.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields

# lot Attribute Value 
class LotAttributeValue(models.Model):
    _name = "lot.attribute.value"
    _order = 'sequence, attribute_id, id'

    name = fields.Char('Value', required=True, translate=True)
    sequence = fields.Integer('Sequence', help="Determine the display order")
    attribute_id = fields.Many2one('lot.attribute', 'Attribute', ondelete='cascade', required=True)

#Lot Attribute Line  
class LotAttributeLine(models.Model):
    _name = "lot.attribute.line"
    _rec_name = 'attribute_id'

    product_tmpl_id = fields.Many2one('product.template','Product Template')
    lot_id = fields.Many2one('stock.production.lot','Lot')
    attribute_id = fields.Many2one('lot.attribute', 'Attribute', ondelete='restrict', required=True)
    value_ids = fields.Many2many('lot.attribute.value', string='Attribute Values')
    
#Lot Attribute     
class LotAttribute(models.Model):
    _name = "lot.attribute"
    _description = "Lot Attribute"
    _order = 'sequence, name'

    name = fields.Char('Name', required=True, translate=True)
    value_ids = fields.One2many('lot.attribute.value', 'attribute_id', 'Values', copy=True)
    sequence = fields.Integer('Sequence', help="Determine the display order")
    attribute_line_ids = fields.One2many('lot.attribute.line', 'attribute_id', 'Lines')
    create_variant = fields.Boolean(default=True, help="Check this if you want to create multiple variants for this attribute.")
