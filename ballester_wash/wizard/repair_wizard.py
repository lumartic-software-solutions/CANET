# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
import pytz
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class RepairWizard(models.TransientModel):

    _name = "repair.wizard"


    @api.multi
    def create_repair(self):
        ctx = self._context
        if ctx.get('active_id'):
            wash_obj = self.env['wash.order']
            brw_wash  = wash_obj.browse(ctx.get('active_id'))
            if brw_wash:
                repair_vals = {
			'wash_id':ctx.get('active_id'),
			'name' : self.env['ir.sequence'].next_by_code('mrp.repair'),
                        'product_id': brw_wash.product_id.id,
			'product_qty': brw_wash.product_qty,
			'product_uom': brw_wash.product_uom.id,
			'location_id':  brw_wash.location_id.id,
                        'location_dest_id' : brw_wash.location_dest_id.id,
			'lot_id': brw_wash.lot_id.id,
			'invoice_method':  'none',
			'operations': brw_wash.operations,
			}
                repair_obj = self.env['mrp.repair']
                repair_id = repair_obj.create(repair_vals)
                action = self.env.ref('mrp_repair.action_repair_order_tree').read()[0]
                action['views'] = [(self.env.ref('mrp_repair.view_repair_order_form').id, 'form')]
                action['res_id'] = repair_id.id
                brw_wash.state = 'repair_create'
                return action
