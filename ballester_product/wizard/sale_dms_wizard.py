# -*- coding: utf-8 -*-
# Odoo, Open Source Ballester Product.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api,_
from datetime import datetime
from odoo.tools.float_utils import float_compare


#add document wizard in sale
class DMSfile(models.Model):
    _inherit = 'muk_dms.file'   
    
    sale_id = fields.Many2one('sale.order','Sale') 
    
    @api.model
    def default_get(self,default_fields):
        res = super(DMSfile, self).default_get(default_fields)
        ctx = dict(self._context)
        if ctx.get('active_model') == 'sale.order':
            dms_directory_id = self.env['ir.config_parameter'].sudo().get_param('default_sale_dms_id')
            if dms_directory_id:
                res.update({'directory': int(dms_directory_id) })
            if ctx.get('active_id'):   
                res.update({'sale_id': ctx.get('active_id') })
        return res


 
