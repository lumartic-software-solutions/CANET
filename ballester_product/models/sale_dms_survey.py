# -*- coding: utf-8 -*-
# Odoo, Open Source Ballester Product.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api,_
from datetime import datetime
from odoo.tools.float_utils import float_compare
from ast import literal_eval


class Sale(models.Model):
    _inherit = "sale.order"
    
    
    @api.multi
    def action_view_document(self):
        files = self.mapped('file_ids')
        action = self.env.ref('muk_dms.action_dms_file').read()[0]
        if len(files) > 1:
            action['domain'] = [('id', 'in', files.ids)]
        elif len(files) == 1:
            action['views'] = [(self.env.ref('muk_dms.view_dms_file_form').id, 'form')]
            action['res_id'] = files.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    
    @api.depends( 'file_ids')
    def _get_file(self):
        """
        Count the document of a SO.:

        """
        for order in self:
            total_file = len(order.file_ids) 
            order.update({
                'file_count': total_file,
            })
            
    file_ids = fields.One2many('muk_dms.file','sale_id','Documents')
    file_count = fields.Integer(string='Documents', compute='_get_file', readonly=True)
    
    
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    #directory field for configuration in sale
    default_sale_dms_id = fields.Many2one(
        'muk_dms.directory',
        'Sale Directory',)
    
    #store directory value
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        default_sale_dms_id = literal_eval(ICPSudo.get_param('default_sale_dms_id', default='False'))
        res.update(
            default_sale_dms_id=default_sale_dms_id,
        )
        return res
    
    #store directory value
    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param("default_sale_dms_id", self.default_sale_dms_id.id)
