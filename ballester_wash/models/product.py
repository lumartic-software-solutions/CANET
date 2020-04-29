# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare
    
# new fields 
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    recycled = fields.Boolean('Recycled')
    type_of_drum = fields.Selection([('plastic','Plastic Drum'),('metal','Metal Drums')],'Type Of Drum')
    dangerous = fields.Boolean('Dangerous')
    wash_product = fields.Boolean ('Is it Wash Product?')
    non_dangerous = fields.Boolean('Non-Dangerous')
    cage = fields.Boolean('Cage')
    plastic_kg = fields.Integer('Plastic Kg.')
    metal_kg = fields.Integer('Metal Kg.')


class DangerousProduct(models.Model):
    _name = 'dangerous.product'


    product_id = fields.Many2one('product.template', 'Dangerous Product', domain="[('type','=','consu')]")
    dangerous = fields.Boolean('Dangerous')
    non_dangerous = fields.Boolean('Non-Dangerous') 
    type_product = fields.Selection([('container','Container'),('drum','Drum')],'Type')  
    qty = fields.Float('Quantity')
 

    @api.model
    def create(self ,vals):
        ctx = self._context
        result = super(DangerousProduct,self).create(vals)
        if ctx.get('default_dangerous'):
            product = result.product_id
            product.write({'dangerous': True,'wash_product':True ,'non_dangerous':False})
            result.update({'dangerous':True})
        if ctx.get('default_non_dangerous'):
            product = result.product_id
            result.update({'non_dangerous':True})
            product.write({'non_dangerous':True,'wash_product':True, 'dangerous':False})
        return result
   

    
# new fields 
class ProductProduct(models.Model):
    _inherit = 'product.product'


    recycled_product_id = fields.Many2one('product.product','Recycled Product')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=900):
        if args is None:
            args = []
        pro_ids = []
        pro_service_ids = []
        ctx = self._context
        param_obj = self.env['ir.config_parameter']
        sddr_ids = self.env.ref('ballester_wash.product_param_1_id')
        location_obj = self.env['stock.location']
        quant_obj = self.env['stock.quant']
        residupes_ids = self.env.ref('ballester_wash.product_param_3_id')
        container_ids = self.env.ref('ballester_wash.product_param_2_id')
        drum_ids = self.env.ref('ballester_wash.product_param_4_id')
        '''if ctx.get('type_of_order') == 'container' or ctx.get('type_of_order') == 'drum'  :
            if sddr_ids and residupes_ids :
                sddr_id = int(sddr_ids.value)
                residupes_id = int(residupes_ids.value)
                category_container_id = self.env['product.category'].search([('id','in',[sddr_id, residupes_id])])
                if category_container_id:
                    product_search_ids = self.search([('categ_id','in',[cat.id for cat in category_container_id])])
                    if product_search_ids:'''
        if ctx.get('location_id'):
            location_search = location_obj.browse(ctx.get('location_id'))
            quant_search = quant_obj.search([('location_id','=', location_search[0].id)])
            if quant_search:
                pro_ids = [pro.product_id.id for pro in quant_search]
                       #pro_ids = [pro.id for pro in product_search_ids]
                args += [('id','in', pro_ids)]
            else:
                args = [('id', 'in', [])]
        if ctx.get('source_location_id'):
            location_search = location_obj.browse(ctx.get('source_location_id'))
            quant_search = quant_obj.search([('location_id','=', location_search[0].id)])
            service_product_search = self.search([('type','=','service')])
            if quant_search:
                pro_ids = [pro.product_id.id for pro in quant_search]
                       #pro_ids = [pro.id for pro in product_search_ids]
                if service_product_search:
                     pro_service_ids = [pro.id for pro in service_product_search]
                     pro_ids = pro_ids + pro_service_ids
                args += [('id','in', pro_ids)]
            else:
                if service_product_search:
                     pro_service_ids = [pro.id for pro in service_product_search]
                args = [('id', 'in', pro_service_ids)]
        
        if ctx.get('model') == 'sale.order.line'  and  not ctx.get('source_location_id') :
            raise UserError(_('Please select source location first.'))
        
        if ctx.get('recycle') and ctx.get('type') == 'container':
            if container_ids and sddr_ids:
                sddr_id = int(sddr_ids.value) 
                container_id=int(container_ids.value)
                category_re_id = self.env['product.category'].search([('id','in',[container_id, sddr_id])])
                if category_re_id:
                    product_search_ids = self.search([('categ_id','=',[cat.id for cat in category_re_id])])
                    if product_search_ids:
                        pro_ids = [pro.id for pro in product_search_ids]
                        
                        args += [('id','in', pro_ids)]
        if ctx.get('recycle') and ctx.get('type') == 'drum':
            if sddr_ids and drum_ids :
                drum_id =  int(drum_ids.value)
                sddr_id = int(sddr_ids.value)
                category_re_id = self.env['product.category'].search([('id','in',[sddr_id,drum_id])])
                if category_re_id:
                    product_search_ids = self.search([('categ_id','=',[cat.id for cat in category_re_id])])
                    if product_search_ids:
                        pro_ids = [pro.id for pro in product_search_ids]
                        args += [('id','in', pro_ids)]
        print ("---------------args",args)
        recs = super(ProductProduct,self).name_search(name,args=args, operator=operator, limit=limit )
        return recs
         
