# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare
    
# new fields 
class MrpReair(models.Model):
    _inherit = 'mrp.repair'
    
    wash_id = fields.Many2one('wash.order','Wash order')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('cancel', 'Cancelled'),
        ('confirmed', 'Confirmed'),
        ('under_repair', 'Under Repair'),
        ('ready', 'Ready to Repair'),
        ('2binvoiced', 'To be Invoiced'),
        ('invoice_except', 'Invoice Exception'),
        ('done', 'Repaired'),('check_compliance', 'Checked Compliance')], string='Status',
        copy=False, default='draft', readonly=True, track_visibility='onchange',
        help="* The \'Draft\' status is used when a user is encoding a new and unconfirmed repair order.\n"
             "* The \'Confirmed\' status is used when a user confirms the repair order.\n"
             "* The \'Ready to Repair\' status is used to start to repairing, user can start repairing only after repair order is confirmed.\n"
             "* The \'To be Invoiced\' status is used to generate the invoice before or after repairing done.\n"
             "* The \'Done\' status is set when repairing is completed.\n"
             "* The \'Cancelled\' status is used when user cancel repair order.")  
    timesheet_ids = fields.One2many('account.analytic.line','repair_id', 'Time Parts')
    start_datetime = fields.Datetime('Start Repair Time')
    
    

    @api.multi
    def action_back_wash_order(self):
        if self.wash_id.type_of_order == 'drum':
            action = self.env.ref('ballester_wash.action_wash_order_tree_drum')
        if self.wash_id.type_of_order == 'container':
            action = self.env.ref('ballester_wash.action_wash_order_tree_container')
        result = action.read()[0]
        res = self.env.ref('ballester_wash.view_wash_order_form', False)
        result['views'] = [(res and res.id or False, 'form')]
        result['res_id'] = self.wash_id.id
        return result
    
    
    
