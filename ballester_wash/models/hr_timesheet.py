# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare
    
# new fields 
class HrTimesheet(models.Model):
    _inherit = 'account.analytic.line'

    wash_id = fields.Many2one('wash.order', 'Wash')
    time = fields.Char('Wash Time')
    repair_id  = fields.Many2one('mrp.repair')


