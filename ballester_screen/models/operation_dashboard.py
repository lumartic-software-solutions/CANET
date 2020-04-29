# -*- coding: utf-8 -*-
# Odoo, Open Source Ballester Screen.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#

from odoo import models, fields, api, _
from odoo.http import request
from odoo.exceptions import UserError
from dateutil import parser
from datetime import datetime
import pytz


class OperationDashboard(models.Model):
    _name = "operation.dashboard"

    name = fields.Char(string="Name")


    @api.multi
    @api.returns('stock.warehouse', lambda value: value.id)
    def get_warehouse(self):
        """ Returns warehouse id of warehouse that contains location """
        return self.env['stock.warehouse'].search([
        ('view_location_id.parent_left', '<=', self.parent_left),
        ('view_location_id.parent_right', '>=', self.parent_left)], limit=1)

    # main dashboard method to send all details
    @api.model
    def get_operation_info(self):
        uid = request.session.uid
        ctx = dict(self._context)
        lot_obj = self.env['stock.production.lot']
        location_obj = self.env['stock.location']
        product_obj = self.env['product.product']
        user_id = self.env['res.users'].sudo().search_read([('id', '=', uid)], limit=1)
        product_list = []
        #internal_product_list = []
        location_list = []
        barcode_list = []
        used_barcode_list = []
        unused_barcode_list = []
        unsed_wash_barcode_list =[]
        recycled_product = ''
        recycled_product_list = []
        product_ids = product_obj.search([('sale_ok', '=', True), ('type', '=', 'product')])
        for data in product_ids:
            set_product = self.set_product_name(data)
            set_product_name = ''
            if "''" in set_product:
                set_product_name = set_product.replace("''", "*")
            else:
                set_product_name = set_product.replace('"', "*")
            product_list.append({'name': set_product_name or '',
                                 'id': str(data.id) or '',
                                 'default_code': data.default_code or '',
                                 'ler_code': "[%s] %s" % (
                                 data.lercode_id.name, data.lercode_id.description) if data.lercode_id else 'None',
                                 })
            '''internal_product_list.append({'name': set_product_name or '',
                                          'id': str(data.id) or '',
                                          'default_code': data.default_code or '',
                                          'recycled_product_id': data.recycled_product_id.id or ''
                                          })'''

        if product_list:
            recycled_product = '<select class="product_recycled onchange_product"  id="my-recycled-product" style="height: 45px;font-size: 22px;margin-top: 20px;">'
            for line in product_list:
                recycled_product += '<option label="' + line['name'] + '" ids="' + line['id'] + '"' + ' value="' + line[
                    'name'] + '">' + line['name'] + '</option>'
            recycled_product += '</select>'

        sample_product_id = self.env.ref('ballester_screen.sample_product_id').id
        unused_barcode_ids = lot_obj.search([('product_id', '=', sample_product_id)])
        for data in unused_barcode_ids:
            unused_barcode_list.append({'barcode': data.name or '',
                                        'id': str(data.id) or '',
                                        })
        barcode_ids = lot_obj.search([('product_id', '=', sample_product_id)], limit=1000)
        used_barcode_ids = lot_obj.search([('product_id', '!=', sample_product_id)], limit=1000)
        for data in barcode_ids:
            barcode_list.append({'barcode': data.name or '',
                                 'id': str(data.id) or '',
                                 })
        for data in used_barcode_ids:
            used_barcode_list.append({'barcode': data.name or '',
                                      'id': str(data.id) or '',
                                      })

        search_wash_order = self.env['wash.order'].search([])
        unsed_wash_barcode_list_ids = lot_obj.search([('id', 'not in', [ wash.lot_id.id for wash in search_wash_order])])
        for data in unsed_wash_barcode_list_ids:
            unsed_wash_barcode_list.append({'barcode': data.name or '',
                                        'id': str(data.id) or '',
                                        })
        location_ids = location_obj.search([('usage', 'in', ['internal'])])
        for location in location_ids:
            orig_location = location
            name = location.name
            while location.location_id and location.usage != 'view':
                location = location.location_id
                if not name:
                    raise UserError(_('You have to set a name for this location.'))
                name = location.name + "/" + name
            location_list.append({'name': name or '',
                                  'id': str(orig_location.id) or '',
                                  })
        product_selection = ''
        barcode_selection = ''
        if len(product_list) > 0:
            product_selection = '<select class="products" style="overflow-y: auto!important; font-size: 18px;">'
            for line in product_list:
                product_selection += '<option label="' + line['default_code'] + '" ids="' + line[
                    'id'] + '"' + ' value="' + line['name'] + '" product_ler_code="' + line['ler_code'] + '">' + line[
                                         'name'] + '</option>'
            product_selection += '</select>'
        else:
            product_selection = '<select class="products" style="overflow-y: auto!important; font-size: 18px;"><option> No Data Found !</option> </select>'
        if len(barcode_list) > 0:
            barcode_selection = '<select class="barcodes" style="overflow-y: auto!important; font-size: 18px;">'
            for line in barcode_list:
                barcode_selection += '<option ids="' + line['id'] + '"' + ' value="' + line['barcode'] + '">' + line[
                    'barcode'] + '</option>'
            barcode_selection += '</select>'
        else:
            barcode_selection = '<select class="barcodes" style="overflow-y: auto!important; font-size: 18px;"><option> No Data Found ! </option> </select>'
        set_unused_barcode_list = False

        if len(unused_barcode_list) > 0:
            set_unused_barcode_list = True
        if recycled_product:
            recycled_product = recycled_product
        else:
            recycled_product = recycled_product_list
        if user_id:
            data = {
                'product_list': product_selection,
               # 'internal_product_list': internal_product_list,
                'barcode_list': barcode_selection,
                'location_list': location_list,
                'set_product_list': product_list,
                'set_barcode_list': barcode_list,
                'used_set_barcode_list': used_barcode_list,
		'unsed_wash_barcode_list' : unsed_wash_barcode_list,
                'unused_barcode_list': unused_barcode_list,
                'set_unused_barcode_list': set_unused_barcode_list,
                'type_of_order': [{'order': 'Container'}, {'order': 'Drum'}],
		'washing_type': [{'washing': 'dangerous'}, {'washing': 'non_dangerous'}],
            }
            user_id[0].update(data)
            return user_id
        else:
            raise UserError(_('Login User Is Not Set As Employee!'))


    @api.model
    def product_data(self , domain):
        if domain:
            product_search = self.env['product.product'].search(domain)
            display_name = ''
            lot_list = []
            if product_search:
                lot_product_search = self.env['stock.production.lot'].search([('product_id','=', product_search[0].id)])
                if product_search[0].recycled_product_id:
                    display_name = product_search[0].recycled_product_id.display_name
                if lot_product_search:
                    for lot in lot_product_search:
                        lot_list.append({
				'name' : lot.name,
				'id' :lot.id,}
				)
                return {'product_name':  display_name , 'lot_list':lot_list}
        else:
            return {}


    @api.model
    def location_data(self , location1,location2,length):
        location_obj = self.env['stock.location']
        location_search = False
        if location1 or location2:
            if length >= 3:
                parent_location_search =  location_obj.search([('name','=' ,str(location1))])
                prent_of_parent_search= location_obj.search([('location_id','=' ,parent_location_search[0].id)])
                location_search = location_obj.search([('name','=' ,str(location2)), ('location_id','=', prent_of_parent_search[0].id)])
            else:
                parent_location_search =  location_obj.search([('name','=' ,str(location1))])
                location_search = location_obj.search([('name','=' ,str(location2)), ('location_id','=', parent_location_search[0].id)])
            lot_list = []
            wash_list =[]
            wash_ids = self.env['wash.order'].search(['|',('location_id','=', location_search[0].id),('location_dest_id','=', location_search[0].id)])
            if wash_ids:
                for wash in wash_ids:
                    wash_list.append(wash.lot_id.id)
            if location_search:
                if wash_list:
                    quant_search_ids = self.env['stock.quant'].search([('location_id','=', location_search[0].id),('lot_id','not in',wash_list )])
                else:
                    quant_search_ids = self.env['stock.quant'].search([('location_id','=', location_search[0].id)])
                if quant_search_ids:
                    for quant in quant_search_ids:
                        lot_list.append({
				'name' : quant.lot_id.name,
				'id' :quant.lot_id.id,
				})
                         

            
                return {'lot_list':lot_list}
        else:
            return {}


    @api.model
    def categ_data(self ,name ):
        categ_ids = self.env['product.category'].search([('name','=',name)])
        product_list = []
        if categ_ids:
                product_ids= self.env['product.product'].search([('categ_id','=',categ_ids[0].id )])
                if product_ids:
                    for pro in product_ids:
                        set_product = self.set_product_name(pro)
                        set_product_name = ''
                        if "''" in set_product:
                            set_product_name = set_product.replace("''", "*")
                        else:
                            set_product_name = set_product.replace('"', "*")
                        product_list.append({'name': set_product_name or '',
                                 'id': str(pro.id) or '',
                                 'default_code': pro.default_code or '',
				 'ler_code': "[%s] %s" % (
                                 pro.lercode_id.name, pro.lercode_id.description) if pro.lercode_id else 'None',
                                 })
                product_selection = ''
                if len(product_list) > 0:
                    product_selection = '<select class="products" style="overflow-y: auto!important; font-size: 18px;">'
                    for line in product_list:
                        product_selection += '<option label="' + line['default_code'] + '" ids="' + line[
                         'id'] + '"' + ' value="' + line['name'] + '" product_ler_code="' + line['ler_code'] +  '">' + line[
                                         'name'] + '</option>'
                    product_selection += '</select>'
                else:
                    product_selection = '<select class="products" style="overflow-y: auto!important; font-size: 18px;"><option> No Data Found !</option> </select>'
                        
                return {'product_selection':product_selection,
			'cat_product_list': product_list}
        else:
            return {}


    @api.model
    def lot_data(self ,doamin):
        location_search = False
        if doamin:
            lot_ids =  self.env['stock.production.lot'].search(doamin)
            if lot_ids:
                display_name = lot_ids.product_id.default_code
                recycled_display_name = lot_ids.product_id.recycled_product_id.default_code
                return {'product_name':  display_name , 'recycled_product_name':recycled_display_name}
        else:
            return {}

    @api.model
    def get_inventory_adjustment_info(self):
        uid = request.session.uid
        ctx = dict(self._context)
        location_obj = self.env['stock.location']
        categ_obj =  self.env['product.category']
        location_list = []
        category_list = []
        location_ids = location_obj.search([('usage', 'in', ['internal'])])
        category_ids = categ_obj.search([])
        for location in location_ids:
            orig_location = location
            name = location.name
            while location.location_id and location.usage != 'view':
                location = location.location_id
                if not name:
                    raise UserError(_('You have to set a name for this location.'))
                name = location.name + "/" + name
            location_list.append({'name': name or '',
                                  'id': str(orig_location.id) or '',
                                  })

        for categ in category_ids:
            orig_categ = categ
            name = categ.name
            category_list.append({'name': name or '',
                                  'id': str(orig_categ.id) or '',
                                  })
        print ("^^^^^^^^^^^^^^^category_list",category_list)
       
        data = {
              #  'product_list': product_list,
                'location_list': location_list,
		'category_list' : category_list,
            }
        return {'data' : data}
	
    @api.model
    def get_internal_transfer_info(self):
        uid = request.session.uid
        ctx = dict(self._context)
        print ("ddddd>>>>>>>>>>>>>>>ddddddd", ctx)
        lot_obj = self.env['stock.production.lot']
        location_obj = self.env['stock.location']
        product_obj = self.env['product.product']
        location_list = []
        unsed_wash_barcode_list= []

        self._cr.execute('''select * from wash_order''')
        wash_result = self._cr.dictfetchall()
        wash_barcode_ids =  tuple([ wash.get('lot_id') for wash in wash_result])
        params = {'wash_barcode_ids': wash_barcode_ids}
        if wash_barcode_ids:
            self._cr.execute('''select * from stock_production_lot where id not in %(wash_barcode_ids)s''',params)
            unsed_wash_barcode_list_ids = self._cr.dictfetchall()
            for data in unsed_wash_barcode_list_ids:
                unsed_wash_barcode_list.append({'barcode': data.get('name') or '',
                                        'id': str(data.get('id')) or '',
                                        })

        search_wash_order = self.env['wash.order'].search([])
        location_ids = location_obj.search([('usage', 'in', ['internal'])])
        for location in location_ids:
            orig_location = location
            name = location.name
            while location.location_id and location.usage != 'view':
                location = location.location_id
                if not name:
                    raise UserError(_('You have to set a name for this location.'))
                name = location.name + "/" + name
            location_list.append({'name': name or '',
                                  'id': str(orig_location.id) or '',
                                  })
        data = {
              #  'product_list': product_list,
                'barcode_list': unsed_wash_barcode_list,
                'location_list': location_list,
                'type_of_order': [{'order': 'Container'}, {'order': 'Drum'}],
		'washing_type': [{'washing': 'dangerous'}, {'washing': 'non_dangerous'}],
            }
        return {'data' : data}

    # create barcode 
    @api.multi
    def create_barcode(self, number_of_barcode):
        if number_of_barcode == '':
            return {'warning': 'No Data Found!'}
        if int(number_of_barcode) > 0:
            created_barcode_data = []
            created_barcode_ids = []
            number = int(number_of_barcode)
            count = 0
            for rec in range(number):
                count += 1
                barcode_sequence = self.env['ir.sequence'].next_by_code('ballester.stock.production.lot') or _('New')
                vals = {'barcode': barcode_sequence}
                product_id = self.env.ref('ballester_screen.sample_product_id').id
                lot_vals = {'product_id': product_id or False,
                            'name': barcode_sequence or '',
                            }
                lot_id = self.env['stock.production.lot'].create(lot_vals)
                vals.update({'count': count})
                created_barcode_data.append(vals)
                created_barcode_ids.append(lot_id.id)
            return {'success': _('Successfully Created the Barcode!'), 'created_barcode_ids': created_barcode_ids,
                    'created_barcode_data': created_barcode_data}
        else:
            return {'warning': 'Please Enter Valid Number !'}

    # creating Wash Order
    @api.multi
    def create_wash_order_method(self, record_data):
        inventory_obj = self.env['stock.inventory']
        lot_obj = self.env['stock.production.lot']
        location_obj= self.env['stock.location']
        product_obj = self.env['product.product']
        inventory_adjustment_table = []
        ctx = dict(self._context)
        name = False
        user = self.env.uid
        brw_usr = self.env['res.users'].search([('id','=',user)])
        type_of_order = False
        location_dest_search = False
        location_search = False
        dangerous_obj = self.env['dangerous.product']
        args = brw_usr.company_id and [('company_id', '=', brw_usr.company_id.id)] or []
        warehouse = self.env['stock.warehouse'].search(args, limit=1)
        drum_wash_line= []
        container_wash_line = []
        create_wash_order = False
        user_tz = self.env.user.tz
        local = pytz.timezone(user_tz)
        date = datetime.now(local)
        for data in record_data:
            if data.get('washing_type'):
                if data.get('washing_type') == 'dangerous':
                    self.dangerous = True
                    self.non_dangerous = False
     		    
                    dangerous_product_con_ids =dangerous_obj.search([('type_product','=','container'),('dangerous','=', True)])
                    dangerous_product_drum_ids = dangerous_obj.search([('type_product','=','drum'),('dangerous','=', True)])
                    if  dangerous_product_con_ids:
                        if data.get('type_of_order') == 'Container':
                            container_wash_line = []
                            for product  in dangerous_product_con_ids:
                                vals = {
                               'product_id': product.product_id.product_variant_id.id,
                                'type':'add',
                                'name':product.product_id.display_name,
                                'product_uom_qty':product.qty,
                                'product_uom': product.product_id.uom_id.id,
				'location_dest_id': self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id,
				'location_id': warehouse.lot_stock_id.id,
				'price_unit':0.0
                                  }
                                container_wash_line.append((0,0,vals))
                    if dangerous_product_drum_ids:
                        if data.get('type_of_order') == 'Drum':
                            drum_wash_line = []
                            for product  in dangerous_product_drum_ids:
                                vals = {
                               'product_id':product.product_id.product_variant_id.id,
                                'type':'add',
                                'name':product.product_id.display_name,
                                'product_uom_qty':product.qty,
                                'product_uom': product.product_id.uom_id.id,
				'location_dest_id': self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id,
				'location_id': warehouse.lot_stock_id.id,
				'price_unit':0.0
                                  }
                                drum_wash_line.append((0,0,vals))
                if data.get('washing_type') == 'non_dangerous':
                    self.non_dangerous = True
                    self.dangerous = False
                    nondangerous_product_con_ids =dangerous_obj.search([('type_product','=','container'),('non_dangerous','=', True)])
                    nondangerous_product_drum_ids = dangerous_obj.search([('type_product','=','drum'),('non_dangerous','=', True)])
                    if  nondangerous_product_con_ids:
                        if data.get('type_of_order') == 'Container':
                            container_wash_line = []
                            for product  in nondangerous_product_con_ids:
                                vals = {
                               'product_id': product.product_id.product_variant_id.id,
                                'type':'add',
                                'name':product.product_id.display_name,
                                'product_uom_qty':product.qty,
                                'product_uom': product.product_id.uom_id.id,
				'location_dest_id': self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id,
				'location_id': warehouse.lot_stock_id.id,
				'price_unit': 0.0
                                  }
                                container_wash_line.append((0,0,vals))
                    if nondangerous_product_drum_ids:
                        if data.get('type_of_order')== 'Drum':
                            drum_wash_line = []
                            for product  in nondangerous_product_drum_ids:
                                vals = {
                               'product_id':product.product_id.product_variant_id.id,
                                'type':'add',
                                'name':product.product_id.display_name,
                                'product_uom_qty':product.qty,
                                'product_uom': product.product_id.uom_id.id,
				'location_dest_id': self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id,
				'location_id': warehouse.lot_stock_id.id,
                                  'price_unit':0.0}
                                drum_wash_line.append((0,0,vals))
            if data.get('location'):
                name_location = data.get('location')
                name = name_location.split('/')[-1]
                spilt_name = name_location.split('/')
                name = spilt_name[-1]
                parent_name = spilt_name[0]
                parent_loc_id = location_obj.search([('name','=',parent_name)])
                location_search = location_obj.search([('name','=',name),('location_id','=',  parent_loc_id[0].id or False)])
                if location_search:
                    location_search = location_search[0].id
            if data.get('dest_location_id'):
                name_dest_location = data.get('dest_location_id')
                spilt_name = name_dest_location.split('/')
                name = spilt_name[-1]
                parent_name = spilt_name[0]
                parent_loc_id = location_obj.search([('name','=',parent_name)])
                location_dest_search = location_obj.search([('name','=',name),('location_id','=',  parent_loc_id[0].id or False)])
                if location_dest_search:
                    location_dest_search = location_dest_search[0].id
            operation_data = []
            if drum_wash_line:
                operation_data = drum_wash_line
            if container_wash_line:
                operation_data = container_wash_line
            for barcode in data.get('barcode_ids'):
                
                if data.get('type_of_order') == 'Container':
                    type_of_order = 'container'
                    name = self.env['ir.sequence'].next_by_code('wash.order.container') or _('New')
                if data.get('type_of_order') == 'Drum':
                    type_of_order = 'drum'
                    name = self.env['ir.sequence'].next_by_code('wash.order.drum') or _('New')
                lot_brw = self.env['stock.production.lot'].browse(int(barcode))
                wash_data = {
                    'name': name,
                    'type_of_order': type_of_order,
                    'product_id': lot_brw[0].product_id.id,
                    'recycled_product_id': lot_brw[0].product_id.recycled_product_id.id,
                    'location_id': location_search,
                    'location_dest_id': location_dest_search,
                    'product_qty': 1.0,
                    'product_uom': lot_brw[0].product_id.uom_id.id,
                    'state': 'draft',
		    'wash_date':date,
		    'washing_type' : data.get('washing_type'),
		    'operations': operation_data,
                    'lot_id': int(barcode),
                }
                create_wash_order = self.env['wash.order'].create(wash_data)
            if create_wash_order:
                return {'success': "Successfully Created Wash Order!"}

    

    @api.multi
    def create_internal_transfer_method(self, record_data):
        inventory_obj = self.env['stock.inventory']
        picking_type_obj = self.env['stock.picking.type']
        lot_obj = self.env['stock.production.lot']
        location_obj= self.env['stock.location']
        product_obj = self.env['product.product']
        inventory_adjustment_table = []
        ctx = dict(self._context)
        name = False
        user = self.env.uid
        brw_usr = self.env['res.users'].search([('id','=',user)])
        type_of_order = False
        location_dest_search = False
        location_search = False
        create_internal_order = False
        dangerous_obj = self.env['dangerous.product']
        args = brw_usr.company_id and [('company_id', '=', brw_usr.company_id.id)] or []
        warehouse_id = False
        for data in record_data:
            if data.get('location'):
                name_location = data.get('location')
                name = name_location.split('/')[-1]
                spilt_name = name_location.split('/')
                name = spilt_name[-1]
                parent_name = spilt_name[0]
                parent_loc_id = location_obj.search([('name','=',parent_name)])
                location_search = location_obj.search([('name','=',name),('location_id','=',  parent_loc_id[0].id or False)])
                if location_search:
                    location_search = location_search[0].id
            if data.get('dest_location_id'):
                name_dest_location = data.get('dest_location_id')
                spilt_name = name_dest_location.split('/')
                name = spilt_name[-1]
                parent_name = spilt_name[0]
                parent_loc_id = location_obj.search([('name','=',parent_name)])
                location_dest_search = location_obj.search([('name','=',name),('location_id','=',  parent_loc_id[0].id or False)])
                warehouse_id = location_dest_search.get_warehouse()
                if location_dest_search:
                    location_dest_search = location_dest_search[0].id
            move_line_data =[]
            user_tz = self.env.user.tz
            local = pytz.timezone(user_tz)
            date = datetime.now(local)
            
            for barcode in data.get('barcode_ids'):
            
                lot_brw= lot_obj.browse(int(barcode))
                move_line_vals = {
		'product_id' :lot_brw[0].product_id.id,
		'product_uom_id' : lot_brw[0].product_id.uom_id.id,
		'lot_id': lot_brw.id,
		'lot_name':lot_brw.name,
		'qty_done' : 1.0,
		 'location_id': location_search,
                'location_dest_id': location_dest_search,
		'date':date,
				}
		
                move_line_data.append((0,0,move_line_vals))
            
            
            picking_type_ids = picking_type_obj.search([('warehouse_id','=',warehouse_id[0].id ),('code','=','internal')])
            internal_data = {
			    'location_id': location_search,
			    'location_dest_id': location_dest_search,
			    'scheduled_date': date,
			  # 'move_lines' :product_data,
				'picking_type_id':picking_type_ids[0].id,
				'move_line_ids': move_line_data,
				'name':picking_type_obj.browse(picking_type_ids[0].id).sequence_id.next_by_id()
			    
            }
            create_internal_order = self.env['stock.picking'].with_context(create_move=True).create(internal_data)
            create_internal_order.button_validate()
        if create_internal_order:
            return {'success': "Successfully Created Wash Order!"}


    @api.multi
    def create_destruction_method(self, record_data):
        inventory_obj = self.env['stock.inventory']
        location_obj= self.env['stock.location']
        lot_obj = self.env['stock.production.lot']
        product_obj = self.env['product.product']
        inventory_adjustment_table = []
        print ("xdd----------ddd")
        ctx = dict(self._context)
        location_search = False
        name = False
        user = self.env.uid
        type_of_order = False
        location_dest_search = False
        wash_obj = self.env['wash.order']
        brw_usr = self.env['res.users'].search([('id','=',user)])
        type_of_order = False
        location_dest_search = False
        location_search = False
        dangerous_obj = self.env['dangerous.product']
        args = brw_usr.company_id and [('company_id', '=', brw_usr.company_id.id)] or []
        warehouse = self.env['stock.warehouse'].search(args, limit=1)
        drum_wash_line= []
        create_crush  = False
        create_compact =False
        create_drum_compact= False
        create_drum_crush = False
        container_wash_line = []
        for data in record_data:
            if data.get('location'):
                name_location = data.get('location')
                name = name_location.split('/')[-1]
                spilt_name = name_location.split('/')
                name = spilt_name[-1]
                parent_name = spilt_name[0]
                parent_loc_id = location_obj.search([('name','=',parent_name)])
                location_search = location_obj.search([('name','=',name),('location_id','=',  parent_loc_id[0].id or False)])
                if location_search:
                    location_search = location_search[0].id
            if data.get('dest_location_id'):
                name_dest_location = data.get('dest_location_id')
                spilt_name = name_dest_location.split('/')
                name = spilt_name[-1]
                parent_name = spilt_name[0]
                parent_loc_id = location_obj.search([('name','=',parent_name)])
                location_dest_search = location_obj.search([('name','=',name),('location_id','=',  parent_loc_id[0].id or False)])
                if location_dest_search:
                    location_dest_search = location_dest_search[0].id
            if data.get('washing_type'):
                if data.get('washing_type') == 'dangerous':
                    self.dangerous = True
                    self.non_dangerous = False
     		    
                    dangerous_product_con_ids =dangerous_obj.search([('type_product','=','container'),('dangerous','=', True)])
                    dangerous_product_drum_ids = dangerous_obj.search([('type_product','=','drum'),('dangerous','=', True)])
                    if  dangerous_product_con_ids:
                        if data.get('type_of_order') == 'Container':
                            container_wash_line = []
                            for product  in dangerous_product_con_ids:
                                vals = {
                               'product_id': product.product_id.product_variant_id.id,
                                'type':'add',
                                'name':product.product_id.display_name,
                                'product_uom_qty':product.qty,
                                'product_uom': product.product_id.uom_id.id,
				'location_dest_id': self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id,
				'location_id': warehouse.lot_stock_id.id,
				'price_unit':0.0
                                  }
                                container_wash_line.append((0,0,vals))
                    if dangerous_product_drum_ids:
                        if data.get('type_of_order') == 'Drum':
                            drum_wash_line = []
                            for product  in dangerous_product_drum_ids:
                                vals = {
                               'product_id':product.product_id.product_variant_id.id,
                                'type':'add',
                                'name':product.product_id.display_name,
                                'product_uom_qty':product.qty,
                                'product_uom': product.product_id.uom_id.id,
				'location_dest_id': self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id,
				'location_id': warehouse.lot_stock_id.id,
				'price_unit':0.0
                                  }
                                drum_wash_line.append((0,0,vals))
                if data.get('washing_type') == 'non_dangerous':
                    self.non_dangerous = True
                    self.dangerous = False
                    nondangerous_product_con_ids =dangerous_obj.search([('type_product','=','container'),('non_dangerous','=', True)])
                    nondangerous_product_drum_ids = dangerous_obj.search([('type_product','=','drum'),('non_dangerous','=', True)])
                    if  nondangerous_product_con_ids:
                        if data.get('type_of_order') == 'Container':
                            container_wash_line = []
                            for product  in nondangerous_product_con_ids:
                                vals = {
                               'product_id': product.product_id.product_variant_id.id,
                                'type':'add',
                                'name':product.product_id.display_name,
                                'product_uom_qty':product.qty,
                                'product_uom': product.product_id.uom_id.id,
				'location_dest_id': self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id,
				'location_id': warehouse.lot_stock_id.id,
				'price_unit': 0.0
                                  }
                                container_wash_line.append((0,0,vals))
                    if nondangerous_product_drum_ids:
                        if data.get('type_of_order')== 'Drum':
                            drum_wash_line = []
                            for product  in nondangerous_product_drum_ids:
                                vals = {
                               'product_id':product.product_id.product_variant_id.id,
                                'type':'add',
                                'name':product.product_id.display_name,
                                'product_uom_qty':product.qty,
                                'product_uom': product.product_id.uom_id.id,
				'location_dest_id': self.env['stock.location'].search([('usage', '=', 'production')], limit=1).id,
				'location_id': warehouse.lot_stock_id.id,
                                  'price_unit':0.0}
                                drum_wash_line.append((0,0,vals))

            operation_data = []
            if drum_wash_line:
                operation_data = drum_wash_line
            if container_wash_line:
                operation_data = container_wash_line
            for barcode in data.get('barcode_ids'):
                lot_brw = self.env['stock.production.lot'].browse(int(barcode))
                '''product_record_data = data.get('product_id')
                first_split = product_record_data.split("[")
                second_split = first_split[1].split("]")
                 
                product_search_ids = product_obj.search([('default_code', '=', second_split[0])])'''
                pro_line_values = {  
			    'product_id' :lot_brw[0].product_id.id,
			    'product_uom_id' :lot_brw[0].product_id.uom_id.id,
			    'prod_lot_id' :int(barcode),
			    'product_qty' :0,
			    'location_id' :location_search,
			    'state':'confirm'
			    }
                pro_inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
                pro_inv_vals = {'name' :pro_inventory_sequence,
		       'filter':'product',
		       'line_ids': [(0, 0,  pro_line_values)],
		       'location_id' :location_search,
		       'product_id': lot_brw[0].product_id.id,
		      # 'wash_id': wash_obj.id
			}
                pro_inv = inventory_obj.create(pro_inv_vals)
                pro_inv.action_start()
                pro_inv.action_done()
                if data.get('type_of_order') == 'Container':
                    type_of_order = 'container'
                    crush_container_vals = {  
	                'name':  self.env['ir.sequence'].next_by_code('wash.order.crush'),
			    'product_id' :lot_brw[0].product_id.id,
			    'type_of_order': 'crush',			
			    'product_uom' :lot_brw[0].product_id.uom_id.id,
			    'lot_id' :int(barcode),
			    'product_qty' :0,
			    'location_id' : location_search,
			    'location_dest_id' :location_dest_search,
			   'washing_type' : data.get('washing_type'),
				'operations': operation_data,
			   
			   # 'washing_type': type_of_order,
			     }

                    create_crush = wash_obj.create(crush_container_vals)
                    compact_container_vals = {  
				'name':  self.env['ir.sequence'].next_by_code('wash.order.compact'),
			    'product_id' :lot_brw[0].product_id.id,
			    'type_of_order': 'compact',			
			    'product_uom' :lot_brw[0].product_id.uom_id.id,
			    'lot_id' :int(barcode),
			    'product_qty' :0,
			    'location_id' :location_search,
			    'location_dest_id' :location_dest_search,
				'washing_type' : data.get('washing_type'),
			'operations': operation_data,
			   # 'washing_type': type_of_order,
}
                    create_compact = wash_obj.create(compact_container_vals)
                if data.get('type_of_order') == 'drum':
                    type_of_order = 'drum'
                    if product_search_ids[0].type_of_drum == 'plastic':
                        create_drum_crush = {  
				'name':  self.env['ir.sequence'].next_by_code('wash.order.crush'),
			    'product_id' :lot_brw[0].product_id.id,
			    'type_of_order': 'crush',			
			    'product_uom' :lot_brw[0].product_id.uom_id.id,
			    'lot_id' :int(barcode),
			    'product_qty' :0,
			    'location_id' :location_search,
			    'location_dest_id' :location_dest_search,
			  #  'washing_type': type_of_order,
			'washing_type' : data.get('washing_type'),
				'operations': operation_data,
			     }

                        create_drum_crush = wash_obj.create(crush_container_vals)
                    if product_search_ids[0].type_of_drum == 'metal':
                        compact_container_vals = {  
				'name':  self.env['ir.sequence'].next_by_code('wash.order.compact'),
			    'product_id' :lot_brw[0].product_id.id,
			    'type_of_order': 'compact',			
			    'product_uom' :lot_brw[0].product_id.uom_id.id,
			    'lot_id' :int(barcode),
			    'product_qty' :0,
			    'location_id' :location_search,
			    'location_dest_id' :location_dest_search,
			'operations': operation_data,
			    #'washing_type': type_of_order,
                             }
                        create_drum_compact = wash_obj.create(compact_container_vals)

            if create_crush and create_compact:
                return {'success': "Successfully Created Wash Order!"}
            if create_drum_crush:
                return {'success': "Successfully Created Wash Order!"}
            if create_drum_compact :
                return {'success': "Successfully Created Wash Order!"}


    @api.multi
    def set_product_name(self, product):
        set_product = product.name
        if product.default_code and product.attribute_line_ids:
            variable_attributes = product.attribute_line_ids.filtered(lambda l: len(l.value_ids) > 1).mapped(
                'attribute_id')
            variant = product.attribute_value_ids._variant_name(variable_attributes)
            set_product = variant and "[%s] %s (%s)" % (product.default_code, product.name, variant) or product.name
        else:
            if product.default_code:
                set_product = "[%s] %s" % (product.default_code, product.name)
            elif product.attribute_line_ids:
                variable_attributes = product.attribute_line_ids.filtered(lambda l: len(l.value_ids) > 1).mapped(
                    'attribute_id')
                variant = product.attribute_value_ids._variant_name(variable_attributes)
                set_product = variant and "%s (%s)" % (product.name, variant) or product.name
        return set_product

    @api.multi
    def set_product_name_internal(self, product):
        product_temp_id = product.get('product_tmpl_id')
        product_temp_obj = self.env['product.template'].browse(product_temp_id)
        product_obj = self.env['product.product'].browse(product.get('id'))
        set_product = product_temp_obj.name
        if product.get('default_code') and product_obj.attribute_line_ids:
            variable_attributes = product_obj.attribute_line_ids.filtered(lambda l: len(l.value_ids) > 1).mapped(
                'attribute_id')
            variant = product_obj.attribute_value_ids._variant_name(variable_attributes)
            set_product = variant and "[%s] %s (%s)" % (product.get('default_code'), product_temp_obj.name, variant) or product_temp_obj.name
        else:
            if product.get('default_code'):
                set_product = "[%s] %s" % (product.get('default_code'), product_temp_obj.name)
            elif product_obj.attribute_line_ids:
                variable_attributes = product_obj.attribute_line_ids.filtered(lambda l: len(l.value_ids) > 1).mapped(
                    'attribute_id')
                variant = product_obj.attribute_value_ids._variant_name(variable_attributes)
                set_product = variant and "%s (%s)" % (product_temp_obj.name, variant) or product_temp_obj.name
        return set_product

    # saving inventory adjustments 
    @api.multi
    def save_inventory_adjustments(self, record_data, location_id, created_inventory_id, employee_id):
        barcode_list = []
        for rec in record_data:
            barcode_list.append(int(rec.get('barcode')))
        if len(barcode_list) != len(set(barcode_list)):
            return {'warning': 'The combination of serial number and product must be unique !'}
        if created_inventory_id == 'None':
            # first time saving record
            return self.create_inventory_adjustments_record(record_data, location_id, created_inventory_id, employee_id)
        else:
            # editing record
            return self.edit_inventory_adjustments_record(record_data, location_id, created_inventory_id, employee_id)

    #  saving wash order
    @api.multi
    def save_wash_order_method(self, record_data):
        product_obj = self.env['product.product']
        if record_data:
            for rec in record_data:
                if rec.get('barcode_ids'):
                    lot_ids = self.env['stock.production.lot'].search([('id', 'in', rec.get('barcode_ids'))])
                    if lot_ids:
                        if rec.get('product_id'):
                            product_record_data = rec.get('product_id')
                            first_split = product_record_data.split("[")
                            second_split = first_split[1].split("]")
                            product_search_ids = product_obj.search([('default_code', '=', second_split[0])])
                            for lot in lot_ids:
                                search_wash_ids = self.env['wash.order'].search([('lot_id','=',lot.id)])
                                if search_wash_ids:
                                    for wash in search_wash_ids:
                                        raise UserError(
                                        _('wash order alreday created for this Barcode %s ') % (lot.name)) 
                                if product_search_ids:
                                    if lot.product_id.id != product_search_ids[0].id:
                                        raise UserError(
                                        _('Barcode %s is not associated with wash product %s, please remove it') % (
                                        lot.name, lot.product_id.name))
            return {'success': "Successfully Created The Inventory Adjustments!"}

    #  editing wash order 
    @api.multi
    def edit_wash_order_method(self):
        return {'success': "Successfully Created The Inventory Adjustments!"}

    # creating inventory adjustments 
    @api.multi
    def create_inventory_adjustments_record(self, record_data, location_id, created_inventory_id, employee_id):
        inventory_obj = self.env['stock.inventory']
        lot_obj = self.env['stock.production.lot']
        product_obj = self.env['product.product']
        inventory_adjustment_table = []
        ctx = dict(self._context)
        location = self.env['stock.location'].search([('id', '=', int(location_id))])
        employee = False
        if employee_id:
            employee = self.env['hr.employee'].browse(int(employee_id))
        if not location:
            return {'warning': 'You must select a location !'}
        if len(record_data) != 0 and location != None:
            line_vals = []
            inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
            for rec in record_data:
                product_id = product_obj.search([('id', '=', int(rec.get('product')))], limit=1)
                if product_id:
                    ctx.update({'create_wizard_val': True})
                    lot_id = lot_obj.search([('name', '=', rec.get('barcode'))])
                    if lot_id:
                        lot_id.write({'product_id': product_id.id, 'life_date': rec.get('life_date')})
                        values = {
                            'product_id': product_id.id,
                            'product_uom_id': product_id.uom_id.id,
                            'prod_lot_id': lot_id.id,
                            #                         'theoretical_qty' :0,
                            'product_qty': 1,
                            'location_id': location.id,
                            'state': 'confirm'
                        }
                        line_vals.append(values)
            vals = {'name': inventory_sequence,
                    'filter': 'none',
                    'line_ids': [(0, 0, data) for data in line_vals],
                    'location_id': location.id,
                    'user_id': employee.user_id.id if employee else False,
                    }
            if not created_inventory_id or created_inventory_id == 'None':
                inventory_id = inventory_obj.create(vals)
                inventory_id.action_start()
            else:
                created_inventory_id.write({'line_ids': [(0, 0, data) for data in line_vals]})
                inventory_id = created_inventory_id
            if inventory_id:
                for line in inventory_id.line_ids:
                    life_date = parser.parse(str(line.prod_lot_id.life_date)).strftime('%m/%d/%Y %H:%M:%S')
                    set_product = self.set_product_name(line.product_id)
                    inventory_adjustment_table.append({
                        'name': set_product or '',
                        'prod_lot_id': line.prod_lot_id.name or '',
                        'id': line.id or False,
                        'lot_id': line.prod_lot_id.id or False,
                        'life_date': life_date or '',
                        'ler_code': "[%s] %s" % (line.product_id.lercode_id.name,
                                                 line.product_id.lercode_id.description) if line.product_id.lercode_id else 'None',
                    })
                return {'success': "Successfully Created The Inventory Adjustments!",
                        'inventory_adjustment_table': inventory_adjustment_table, 'id': inventory_id.id}
        else:
            return {'warning': 'No Data Found!'}

    # editing inventory adjustment lines 
    @api.multi
    def edit_inventory_adjustments_record(self, record_data, location_id, created_inventory_id, employee_id):
        inventory_obj = self.env['stock.inventory']
        lot_obj = self.env['stock.production.lot']
        product_obj = self.env['product.product']
        inventory_adjustment_table = []
        inventory_id = inventory_obj.browse(int(created_inventory_id))
        if inventory_id:
            for rec in record_data:
                if 'line_id' not in rec:
                    create_data = [rec]
                    self.create_inventory_adjustments_record(create_data, inventory_id.location_id.id, inventory_id,
                                                             employee_id)
            for line, rec in zip(inventory_id.line_ids, record_data):
                if 'line_id' in rec:
                    if int(rec.get('line_id')) == line.id:
                        product_id = product_obj.search([('id', '=', int(rec.get('product')))], limit=1)
                        if product_id:
                            new_life_date = parser.parse(str(rec.get('life_date'))).strftime('%Y-%m-%d %H:%M:%S')
                            if product_id.id != line.product_id.id:
                                line.product_id = product_id.id
                                lot_id = lot_obj.search([('name', '=', rec.get('barcode'))])
                                lot_id.write({'product_id': product_id.id})
                            if new_life_date != line.prod_lot_id.life_date:
                                line.prod_lot_id.life_date = new_life_date
                            if rec.get('barcode') != line.prod_lot_id.name:
                                prev_lot_id = lot_obj.search([('id', '=', line.prod_lot_id.id)])
                                prev_lot_id.write({'life_date': '',
                                                   'product_id': self.env.ref('ballester_screen.sample_product_id').id})
                                generate_barcode_id = lot_obj.search([('name', '=', rec.get('barcode'))])
                                generate_barcode_id.write({'product_id': product_id.id, 'life_date': new_life_date})
                                line.prod_lot_id = generate_barcode_id.id
                set_product = self.set_product_name(line.product_id)
                life_date = parser.parse(str(line.prod_lot_id.life_date)).strftime('%m/%d/%Y %H:%M:%S')
                inventory_adjustment_table.append({
                    'name': set_product or '',
                    'prod_lot_id': line.prod_lot_id.name or '',
                    'id': line.id or False,
                    'lot_id': line.prod_lot_id.id or False,
                    'life_date': life_date or '',
                    'ler_code': "[%s] %s" % (line.product_id.lercode_id.name,
                                             line.product_id.lercode_id.description) if line.product_id.lercode_id else 'None',
                })
            return {'success': 'Successfully Updated The Inventory Adjustments!',
                    'inventory_adjustment_table': inventory_adjustment_table, 'id': inventory_id.id}
        else:
            return {'warning': 'No Data Found!'}

    # deleting inventory adjustment lines             
    @api.multi
    def delete_inventory_adjustments(self, inventory_id):
        if len(inventory_id) == 1:
            if inventory_id[0] != None:
                inventory_line_ids = self.env['stock.inventory.line'].search([('id', '=', int(inventory_id[0]))])
                if inventory_line_ids:
                    for line in inventory_line_ids:
                        if line.inventory_id.state == 'done':
                            return {'warning': 'You cannot delete a validated inventory adjustement.'}
                        else:
                            line.prod_lot_id.unlink()
                            line.unlink()

                    return {'success': 'Successfully Deleted the Barcode!'}
        else:
            return {'warning': 'You cannot delete inventory adjustement.'}

    # validate inventory adjustments    
    @api.multi
    def validate_inventory_adjustments(self, inventory_list):
        if len(inventory_list) == 1:
            inventory_id = self.env['stock.inventory'].search([('id', '=', inventory_list[0])])
            if inventory_id:
                if inventory_id.state == 'done':
                    return {'warning': 'You cannot delete a validated inventory adjustement.'}
                else:
                    inventory_id.action_done()
                    return {'success': 'Successfully Deleted the Barcode!'}
        else:
            return {'warning': 'You cannot delete inventory adjustement.'}

    # print barcode report
    @api.multi
    def print_barcode(self, inventory_id):
        if len(inventory_id) == 1:
            data = {}
            inventory_line_id = self.env["stock.inventory.line"].search([('id', 'in', inventory_id)], limit=1)
            data['barcode_type'] = 'single'
            data['prod_lot_id'] = inventory_line_id.prod_lot_id.name or ''
            data['product_name'] = inventory_line_id.product_id.name or ''
            return {'data': data}
        else:
            return {'warning': 'No Data Found!'}

    # print generated barcode report
    @api.multi
    def print_generate_barcode(self, barcode_list):
        if len(barcode_list) >= 1:
            data = {}
            record_list = []
            lot_ids = self.env['stock.production.lot'].search([('id', 'in', barcode_list)])
            count = 0
            for rec in lot_ids:
                count += 1
                src = "'/report/barcode/?type=%s&amp;value=%s&amp;width=%s&amp;height=%s'% ('Code128', " + rec.name + ", 600,100)"
                record_list.append({'barcode': rec.name, 'barcode_src': src})
            if len(record_list) >= 1:
                data = {'record_list': record_list, 'barcode_type': 'multi', 'count': count}
                return {'data': data}
        else:
            return {'warning': 'No Data Found!'}
