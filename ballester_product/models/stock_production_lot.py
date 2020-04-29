# -*- coding: utf-8 -*-
# Odoo, Open Source Ballester Product.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api,_
from datetime import datetime
from odoo.tools.float_utils import float_round, float_compare
from odoo.exceptions import UserError


#new fields StockProductionLot
class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    uncode = fields.Char('UN Code')
    lercode_id = fields.Many2one('ler.code','Ler Code')
    admission_parameters= fields.Char('Admission parameters for DA')
    treatement_operation_ids = fields.Many2many('treatement.operation','treatment_lot_rel','treatment_id','lot_id','Treatment Operation')
    danger_char_ids = fields.Many2many('danger.characteristic','danger_lot_rel','danger_id','lot_id','Danger Characteristics')
    attribute_line_ids = fields.One2many('lot.attribute.line', 'lot_id', 'Product Attributes')
    name = fields.Char(
        'Lot/Serial Number', default=lambda self: self.env['ir.sequence'].next_by_code('ballester.stock.production.lot'),
        required=True, help="Unique Lot/Serial Number")
    
    #when change the lercode_id it will set the uncode  
    @api.onchange('lercode_id')
    def onchange_lercode(self):
        if self.lercode_id:
            if self.lercode_id.dangerous == True:
                self.uncode='EMBALAJE VACIO , ,GE III'
            else:
                self.uncode=''
    
    #when change the product_id it will set the general information and table
    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id:
            product_temp_id = self.product_id.product_tmpl_id
            self.uncode = product_temp_id.uncode  or ''
            self.lercode_id = product_temp_id.lercode_id.id  or False
            self.admission_parameters = product_temp_id.admission_parameters  or ''
            self.treatement_operation_ids =[(6, 0, product_temp_id.treatement_operation_ids.ids)] or []
            self.danger_char_ids = [(6, 0, product_temp_id.danger_char_ids.ids)] or []
            self.attribute_line_ids = [(6, 0, product_temp_id.lot_attribute_line_ids.ids)] or [] 
    
    #create the general information and table      
    @api.model
    def create(self,vals):
        res = super(StockProductionLot, self).create(vals)
        if res.product_id:
            product_temp_id = res.product_id.product_tmpl_id
            res.update({ 'uncode' :product_temp_id.uncode  or '',
                        'lercode_id' :product_temp_id.lercode_id.id  or False,
                        'admission_parameters' :product_temp_id.admission_parameters  or '',
                        'treatement_operation_ids' : [(6, 0, product_temp_id.treatement_operation_ids.ids)] or [],
                        'danger_char_ids' :[(6, 0, product_temp_id.danger_char_ids.ids)] or [],
                        'attribute_line_ids': [(6, 0, product_temp_id.lot_attribute_line_ids.ids)] or [] ,
                       })
        return res
    

'''class StockMove(models.Model):
    _inherit = "stock.move"
    
    # Automatically set lot number
    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        self.ensure_one()
        # apply put away
        location_dest_id = self.location_dest_id.get_putaway_strategy(self.product_id).id or self.location_dest_id.id
        vals = {
            'move_id': self.id,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'location_id': self.location_id.id,
            'location_dest_id': location_dest_id,
            'picking_id': self.picking_id.id,
        }
        # set lot name when product is set as unique serial number 
        # pass values of product fields into lot
        if self.product_id.tracking =='serial' :
            product_reference = self.product_id.default_code if self.product_id.default_code else '000'
            sequence = self.env['ir.sequence'].next_by_code('ballester.stock.production.lot') or _('New')
            lot_name = product_reference[:3] + sequence
            vals.update({'lot_name' : lot_name,'qty_done':1})
        if quantity:
            uom_quantity = self.product_id.uom_id._compute_quantity(quantity, self.product_uom, rounding_method='HALF-UP')
            uom_quantity_back_to_product_uom = self.product_uom._compute_quantity(uom_quantity, self.product_id.uom_id, rounding_method='HALF-UP')
            rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            if float_compare(quantity, uom_quantity_back_to_product_uom, precision_digits=rounding) == 0:
                vals = dict(vals, product_uom_qty=uom_quantity)
            else:
                vals = dict(vals, product_uom_qty=quantity, product_uom_id=self.product_id.uom_id.id)
        if reserved_quant:
            if self.product_id.tracking == 'serial' :
                product_vals= {'uncode': self.product_id.uncode or False,
                               'lercode_id' : self.product_id.lercode_id.id or False,
                               'admission_parameters': self.product_id.admission_parameters or False,
                               'treatement_operation_ids':  self.product_id.treatement_operation_ids.ids ,
                               'danger_char_ids': self.product_id.danger_char_ids.ids ,
                               'attribute_line_ids':self.product_id.product_tmpl_id.attribute_line_ids
                                }
                reserved_quant.lot_id.write(product_vals)
            vals = dict(
                vals,
                location_id=reserved_quant.location_id.id,
                lot_id=reserved_quant.lot_id.id or False,
                package_id=reserved_quant.package_id.id or False,
                owner_id =reserved_quant.owner_id.id or False,
            )
        return vals'''
    
    
class StockMoveLine(models.Model):
    _inherit = "stock.move.line"    
    
    def product_field_value(self):
        values={}
        if self.product_id:
            values.update({'uncode': self.product_id.uncode or False,
                           'lercode_id' : self.product_id.lercode_id.id or False,
                           'admission_parameters': self.product_id.admission_parameters or False,
                           'treatement_operation_ids':  self.product_id.treatement_operation_ids.ids ,
                           'danger_char_ids': self.product_id.danger_char_ids.ids ,
                           'attribute_line_ids':self.product_id.product_tmpl_id.attribute_line_ids
                            })
        return values
    
    def _action_done(self):
        """ This method is called during a move's `action_done`. It'll actually move a quant from
        the source location to the destination location, and unreserve if needed in the source
        location.

        This method is intended to be called on all the move lines of a move. This method is not
        intended to be called when editing a `done` move (that's what the override of `write` here
        is done.
        """

        # First, we loop over all the move lines to do a preliminary check: `qty_done` should not
        # be negative and, according to the presence of a picking type or a linked inventory
        # adjustment, enforce some rules on the `lot_id` field. If `qty_done` is null, we unlink
        # the line. It is mandatory in order to free the reservation and correctly apply
        # `action_done` on the next move lines.
        ml_to_delete = self.env['stock.move.line']
        for ml in self:
            # Check here if `ml.qty_done` respects the rounding of `ml.product_uom_id`.
            uom_qty = float_round(ml.qty_done, precision_rounding=ml.product_uom_id.rounding, rounding_method='HALF-UP')
            precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            qty_done = float_round(ml.qty_done, precision_digits=precision_digits, rounding_method='HALF-UP')
            if float_compare(uom_qty, qty_done, precision_digits=precision_digits) != 0:
                raise UserError(_('The quantity done for the product "%s" doesn\'t respect the rounding precision \
                                  defined on the unit of measure "%s". Please change the quantity done or the \
                                  rounding precision of your unit of measure.') % (ml.product_id.display_name, ml.product_uom_id.name))

            qty_done_float_compared = float_compare(ml.qty_done, 0, precision_rounding=ml.product_uom_id.rounding)
            if qty_done_float_compared > 0:
                if ml.product_id.tracking != 'none':
                    picking_type_id = ml.move_id.picking_type_id
                    if picking_type_id:
                        if picking_type_id.use_create_lots:
                            # If a picking type is linked, we may have to create a production lot on
                            # the fly before assigning it to the move line if the user checked both
                            # `use_create_lots` and `use_existing_lots`.
                            if ml.lot_name and not ml.lot_id:
                                values = ml.product_field_value()
                                values.update({'name': ml.lot_name, 'product_id': ml.product_id.id})
                                lot = self.env['stock.production.lot'].create(values)
                                ml.write({'lot_id': lot.id})
                        elif not picking_type_id.use_create_lots and not picking_type_id.use_existing_lots:
                            # If the user disabled both `use_create_lots` and `use_existing_lots`
                            # checkboxes on the picking type, he's allowed to enter tracked
                            # products without a `lot_id`.
                            continue
                    elif ml.move_id.inventory_id:
                        # If an inventory adjustment is linked, the user is allowed to enter
                        # tracked products without a `lot_id`.
                        continue

                    if not ml.lot_id:
                        raise UserError(_('You need to supply a lot/serial number for %s.') % ml.product_id.name)
            elif qty_done_float_compared < 0:
                raise UserError(_('No negative quantities allowed'))
            else:
                ml_to_delete |= ml
        ml_to_delete.unlink()

        # Now, we can actually move the quant.
        done_ml = self.env['stock.move.line']
        for ml in self - ml_to_delete:
            if ml.product_id.type == 'product':
                Quant = self.env['stock.quant']
                rounding = ml.product_uom_id.rounding

                # if this move line is force assigned, unreserve elsewhere if needed
                if not ml.location_id.should_bypass_reservation() and float_compare(ml.qty_done, ml.product_qty, precision_rounding=rounding) > 0:
                    extra_qty = ml.qty_done - ml.product_qty
                    ml._free_reservation(ml.product_id, ml.location_id, extra_qty, lot_id=ml.lot_id, package_id=ml.package_id, owner_id=ml.owner_id)
                # unreserve what's been reserved
                if not ml.location_id.should_bypass_reservation() and ml.product_id.type == 'product' and ml.product_qty:
                    try:
                        Quant._update_reserved_quantity(ml.product_id, ml.location_id, -ml.product_qty, lot_id=ml.lot_id, package_id=ml.package_id, owner_id=ml.owner_id, strict=True)
                    except UserError:
                        Quant._update_reserved_quantity(ml.product_id, ml.location_id, -ml.product_qty, lot_id=False, package_id=ml.package_id, owner_id=ml.owner_id, strict=True)

                # move what's been actually done
                quantity = ml.product_uom_id._compute_quantity(ml.qty_done, ml.move_id.product_id.uom_id, rounding_method='HALF-UP')
                available_qty, in_date = Quant._update_available_quantity(ml.product_id, ml.location_id, -quantity, lot_id=ml.lot_id, package_id=ml.package_id, owner_id=ml.owner_id)
                if available_qty < 0 and ml.lot_id:
                    # see if we can compensate the negative quants with some untracked quants
                    untracked_qty = Quant._get_available_quantity(ml.product_id, ml.location_id, lot_id=False, package_id=ml.package_id, owner_id=ml.owner_id, strict=True)
                    if untracked_qty:
                        taken_from_untracked_qty = min(untracked_qty, abs(quantity))
                        Quant._update_available_quantity(ml.product_id, ml.location_id, -taken_from_untracked_qty, lot_id=False, package_id=ml.package_id, owner_id=ml.owner_id)
                        Quant._update_available_quantity(ml.product_id, ml.location_id, taken_from_untracked_qty, lot_id=ml.lot_id, package_id=ml.package_id, owner_id=ml.owner_id)
                Quant._update_available_quantity(ml.product_id, ml.location_dest_id, quantity, lot_id=ml.lot_id, package_id=ml.result_package_id, owner_id=ml.owner_id, in_date=in_date)
            done_ml |= ml
        # Reset the reserved quantity as we just moved it to the destination location.
        (self - ml_to_delete).with_context(bypass_reservation_update=True).write({
            'product_uom_qty': 0.00,
            'date': fields.Datetime.now(),
        })
