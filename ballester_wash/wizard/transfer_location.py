# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
import pytz
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class TranferLocation(models.TransientModel):

    _name = "transfer.location"

    location_id = fields.Many2one('stock.location','Location')

    wash_name = fields.Char('wash Order')

    @api.model
    def default_get(self, vals):
        res = super(TranferLocation, self).default_get(vals)
        context = self._context
        if  'wash_name' in context:
            wash_ids= self.env['wash.order'].search([('name','=', context.get('wash_name'))])
            if wash_ids :
                res.update({  
                            'wash_name': context.get('wash_name') or False,})
        return res

