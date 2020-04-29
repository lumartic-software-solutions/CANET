# -*- coding: utf-8 -*-
# Odoo, Open Source Ballester Screen.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models, _

    
class LotDetailsWizard(models.TransientModel):
    _name = 'lot.details.wizard'
    _rec_name = 'lot_id'
    
    # set the lot_id and line_id
    @api.model
    def default_get(self, vals):
        res = super(LotDetailsWizard, self).default_get(vals)
        context = self._context
        if  'product_ids' in context and context.get('product_ids') != None  and 'barcode_ids' in context and context.get('barcode_ids') != None:
            product_id = self.env['product.product'].browse(int(context.get('product_ids')))
            barcode_id = self.env['stock.production.lot'].browse(int(context.get('barcode_ids')))
            if product_id and barcode_id:
                product_temp_id = product_id.product_tmpl_id
                res.update({  
                            'lot_id': barcode_id.id or False,
                            'uncode' :product_temp_id.uncode  or '',
                            'lercode_id' :product_temp_id.lercode_id.id  or False,
                            'admission_parameters' :product_temp_id.admission_parameters  or '',
                            'treatement_operation_ids' : [(6, 0, product_temp_id.treatement_operation_ids.ids)] or [],
                            'danger_char_ids' :[(6, 0, product_temp_id.danger_char_ids.ids)] or [],
                            'attribute_line_ids': [(6, 0, product_temp_id.lot_attribute_line_ids.ids)] or [] })
        if 'lot_id'  in context and context.get('lot_id') != None:
            lot_id = self.env['stock.production.lot'].browse(int(context.get('lot_id')))
            if lot_id :
                product_temp_id = lot_id.product_id.product_tmpl_id
                res.update({'lot_id': lot_id.id or False,
                            'uncode' :lot_id.uncode or product_temp_id.uncode or '',
                            'lercode_id' :lot_id.lercode_id.id or product_temp_id.lercode_id.id  or False,
                            'admission_parameters' :lot_id.admission_parameters or product_temp_id.admission_parameters  or '',
                            'treatement_operation_ids' : [(6, 0, lot_id.treatement_operation_ids.ids or product_temp_id.treatement_operation_ids.ids)] or [],
                            'danger_char_ids' :[(6, 0, lot_id.danger_char_ids.ids or product_temp_id.danger_char_ids.ids)] or [],
                            'attribute_line_ids': [(6, 0, lot_id.attribute_line_ids.ids or product_temp_id.lot_attribute_line_ids.ids)] or [] ,
                            })
        if 'line_id'  in context and context.get('line_id') != None :
            line_id = self.env['stock.inventory.line'].browse(int(context.get('line_id')))
            if line_id :
                res.update({'line_id': line_id.id})
                if line_id.inventory_id.state == 'done':
                    res.update({'is_validated': True})
        return res
    
    lot_id = fields.Many2one('stock.production.lot', 'Lots/Serial Numbers')
    line_id = fields.Many2one('stock.inventory.line', 'Inventory Lines')
    uncode = fields.Char('UN Code')
    lercode_id = fields.Many2one('ler.code', 'Ler Code')
    admission_parameters = fields.Char('Admission parameters for DA')
    treatement_operation_ids = fields.Many2many('treatement.operation', 'treatment_lot_rel', 'treatment_id', 'lot_id', 'Treatment Operation')
    danger_char_ids = fields.Many2many('danger.characteristic', 'danger_lot_rel', 'danger_id', 'lot_id', 'Danger Characteristics')
    attribute_line_ids = fields.One2many('lot.attribute.line', 'lot_id', 'Product Attributes')
    is_validated = fields.Boolean('Is Validated Lot details ?', default=False)
    
    @api.onchange('lercode_id')
    def onchange_lercode(self):
        if self.lercode_id:
            if self.lercode_id.dangerous == True:
                self.uncode = 'EMBALAJE VACIO , ,GE III'
            else:
                self.uncode = ''
    
    @api.onchange('attribute_line_ids')
    def _get_onchange_line(self):
        if not self.attribute_line_ids :
            if self.lot_id :
                if self.lot_id.is_created == True and len(self.attribute_line_ids.ids) == 0:
                    self.lot_id.write({'attribute_line_ids': [(6, 0, [])] or []})
                return

    # save button for lot details:
    @api.multi
    def save_lot_details(self):
        if self.lot_id :
            if self.lot_id.is_created == True and len(self.attribute_line_ids.ids) >= 1 :
                self.lot_id.write({
                       'attribute_line_ids': [(6, 0, self.attribute_line_ids.ids)] or [] ,
                                   })
            elif self.lot_id.is_created == False and len(self.attribute_line_ids.ids) >= 1 :
                self.lot_id.write({
                       'attribute_line_ids': [(6, 0, self.attribute_line_ids.ids)] or [] ,
                       'is_created' :True
                                   })
            self.lot_id.write({
                               'uncode' :self.uncode or '',
                               'lercode_id' :self.lercode_id.id or False,
                               'admission_parameters' :self.admission_parameters or '',
                               'treatement_operation_ids' : [(6, 0, self.treatement_operation_ids.ids)]  or [],
                               'danger_char_ids' :[(6, 0, self.danger_char_ids.ids)]  or [],
                               })
            return {'type': 'ir.actions.act_window_close'}
            
