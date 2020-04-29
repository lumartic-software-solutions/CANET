# -*- coding: utf-8 -*-
# Odoo, Open Source Ballester Screen.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#

from odoo import models, fields, api, _
from odoo.http import request
from odoo.exceptions import UserError
from dateutil import parser
from datetime import datetime
import pytz 


class OperationWashDashboard(models.Model):
    _name = "operation.wash.dashboard"

    name = fields.Char(string="Name")


    @api.multi
    def edit_crush_order_method(self):
        return {'success': "Successfully Created The Crush Order!"}

    @api.multi
    def edit_compact_order_method(self):
        return {'success': "Successfully Created The Crush Order!"}
 
    @api.model
    def get_crush_compact_info(self):
        uid = request.session.uid
        ctx = dict(self._context)
        lot_obj = self.env['stock.production.lot']
        location_obj = self.env['stock.location']
        product_obj = self.env['product.product']
        location_list = []
        unsed_wash_barcode_list= []

        self._cr.execute('''select * from wash_order''')
        wash_result = self._cr.dictfetchall()
        wash_barcode_ids =  tuple([ wash.get('lot_id') for wash in wash_result])
        if wash_barcode_ids:
            params = {'wash_barcode_ids': wash_barcode_ids}
            self._cr.execute('''select * from stock_production_lot where id not in %(wash_barcode_ids)s''' ,params)
            unsed_wash_barcode_list_ids = self._cr.dictfetchall()
            for data in unsed_wash_barcode_list_ids:
                unsed_wash_barcode_list.append({'barcode': data.get('name') or '',
                                        'id': str(data.get('id')) or '',
                                        })

        search_wash_order = self.env['wash.order'].search([])
        location_ids = location_obj.search([('usage', 'in', ['internal'])])
        print ("<<<<<<<<<<<<<<<<<<<<<",location_ids )
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

    @api.multi
    def save_crush_order_method(self, record_data):
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
                                if lot.product_id.id != product_search_ids[0].id:
                                    raise UserError(
                                        _('Barcode %s is not associated with wash product %s, please remove it') % (
                                        lot.name, lot.product_id.name))
            return {'success': "Successfully Saved Crush Order!"}

    @api.multi
    def save_compact_order_method(self, record_data):
        product_obj =self.env['product.product']
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
                                if product_search_ids:
                                    if lot.product_id.id != product_search_ids[0].id:
                                        raise UserError(
                                        _('Barcode %s is not associated with wash product %s, please remove it') % (
                                        lot.name, lot.product_id.name))
            return {'success': "Successfully Saved Compact Order!"}


    @api.multi
    def search_type(self, number_of_barcode):
        if number_of_barcode == '':
            return {'warning': 'No Data Found!'}
        if int(number_of_barcode) > 0:
            number =  int(number_of_barcode)
            search_lot_ids = self.env['stock.production.lot'].search([('name','=',number)])
            if search_lot_ids:
                search_wash_order = self.env['wash.order'].search([('type_of_order','=','crush'),('lot_id','=',search_lot_ids[0].id )])
                if  search_wash_order:
                    return {'success':(_('successfully created')) ,'type' : search_wash_order[0].type_of_order}

    @api.multi
    def create_crush_order_method(self, record_data):
        inventory_obj = self.env['stock.inventory']
        location_obj= self.env['stock.location']
        lot_obj = self.env['stock.production.lot']
        product_obj = self.env['product.product']
        inventory_adjustment_table = []
        ctx = dict(self._context)
        name = False
        type_of_order = False
        for data in record_data:
            for barcode in data.get('barcode_ids'):
                type_of_order = 'crush'
                name  = self.env['ir.sequence'].next_by_code('wash.order.crush') or _('New')
                location_search = False
                location_dest_search = False
                if data.get('location'):
                    name_location = data.get('location')
                    first_location_name = name_location.split('/')
                    if len(first_location_name) >= 3:
                        parent_location_search =  location_obj.search([('name','=' ,first_location_name[0])])
                        prent_of_parent_search = location_obj.search([('location_id','=' ,parent_location_search[0].id)])
                        location_search = location_obj.search([('name','=' ,first_location_name[2]), ('location_id','=', prent_of_parent_search[0].id)])
                    else:
                        parent_location_search =  location_obj.search([('name','=' ,first_location_name[0])])
                        location_search = location_obj.search([('name','=' ,first_location_name[-1]), ('location_id','=', parent_location_search[0].id)])
                    if location_search:
                        location_search = location_search[0].id
                if data.get('dest_location_id'):
                    name_dest_location = data.get('location')
                    des_name = name_dest_location.split('/')
                    if len(des_name) >= 3:
                        parent_location_search =  location_obj.search([('name','=' ,des_name[0])])
                        prent_of_parent_search = location_obj.search([('location_id','=' ,parent_location_search[0].id)])
                        location_dest_search = location_obj.search([('name','=' ,des_name[2]), ('location_id','=', prent_of_parent_search[0].id)])
                    else:
                        parent_location_search =  location_obj.search([('name','=' ,des_name[0])])
                        location_dest_search = location_obj.search([('name','=' ,first_location_name[-1]), ('location_id','=', parent_location_search[0].id)])
                    if location_dest_search:
                       location_dest_search = location_dest_search[0].id
                reproduct_search_ids = False
                product_record_data = data.get('product_id')
                first_split = product_record_data.split("[")
                second_split = first_split[1].split("]")
                 
                product_search_ids = product_obj.search([('default_code', '=', second_split[0])])
                if data.get('recycled_product_id'):
                    reproduct_record_data = data.get('recycled_product_id')
                    refirst_split = reproduct_record_data.split("[")
                    resecond_split = refirst_split[1].split("]")
                    reproduct_search_ids = product_obj.search([('default_code', '=', resecond_split[0])])
                user_tz = self.env.user.tz
                local = pytz.timezone(user_tz)
                date = datetime.now(local)
                wash_data = {
                    'name': name,
                    'type_of_order': type_of_order,
                    'product_id': product_search_ids[0].id,
                    'recycled_product_id': reproduct_search_ids[0].id,
                    'location_id': location_search,
                    'location_dest_id': location_dest_search,
                    'wash_date': date,
                    'product_qty': 1.0,
                    'product_uom': product_search_ids.uom_id.id,
                    'state': 'draft',
		    'type_of_drum' :  product_search_ids.type_of_drum,
                    'lot_id': int(barcode),
                }
                create_wash_order = self.env['wash.order'].create(wash_data)
                if create_wash_order:
                    return {'success': "Successfully Created Wash Order!"}

    @api.multi
    def create_compact_order_method(self, record_data):
        inventory_obj = self.env['stock.inventory']
        lot_obj = self.env['stock.production.lot']
        location_obj= self.env['stock.location']
        product_obj = self.env['product.product']
        inventory_adjustment_table = []
        ctx = dict(self._context)
        name = False
        type_of_order = False
        for data in record_data:
            for barcode in data.get('barcode_ids'):
                location_search = False
                location_dest_search = False
                if data.get('location'):
                    name_location = data.get('location')
                    first_location_name = name_location.split('/')
                    if len(first_location_name) >= 3:
                        parent_location_search =  location_obj.search([('name','=' ,first_location_name[0])])
                        prent_of_parent_search = location_obj.search([('location_id','=' ,parent_location_search[0].id)])
                        location_search = location_obj.search([('name','=' ,first_location_name[2]), ('location_id','=', prent_of_parent_search[0].id)])
                    else:
                        parent_location_search =  location_obj.search([('name','=' ,first_location_name[0])])
                        location_search = location_obj.search([('name','=' ,first_location_name[-1]), ('location_id','=', parent_location_search[0].id)])
                    if location_search:
                        location_search = location_search[0].id
                if data.get('dest_location_id'):
                    name_dest_location = data.get('location')
                    des_name = name_dest_location.split('/')
                    if len(des_name) >= 3:
                        parent_location_search =  location_obj.search([('name','=' ,des_name[0])])
                        prent_of_parent_search = location_obj.search([('location_id','=' ,parent_location_search[0].id)])
                        location_dest_search = location_obj.search([('name','=' ,des_name[2]), ('location_id','=', prent_of_parent_search[0].id)])
                    else:
                        parent_location_search =  location_obj.search([('name','=' ,des_name[0])])
                        location_dest_search = location_obj.search([('name','=' ,des_name[-1]), ('location_id','=', parent_location_search[0].id)])
                    if location_dest_search:
                       location_dest_search = location_dest_search[0].id
                type_of_order = 'compact'
                name  = self.env['ir.sequence'].next_by_code('wash.order.compact') or _('New')
                reproduct_search_ids = False
                product_record_data = data.get('product_id')
                first_split = product_record_data.split("[")
                second_split = first_split[1].split("]")
                 
                product_search_ids = product_obj.search([('default_code', '=', second_split[0])])
                if data.get('recycled_product_id'):
                    reproduct_record_data = data.get('recycled_product_id')
                    refirst_split = reproduct_record_data.split("[")
                    resecond_split = refirst_split[1].split("]")
                    reproduct_search_ids = product_obj.search([('default_code', '=', resecond_split[0])])
                user_tz = self.env.user.tz
                local = pytz.timezone(user_tz)
                date = datetime.now(local)
                wash_data = {
                    'name': name,
                    'type_of_order': type_of_order,
                    'product_id': product_search_ids[0].id,
                    'recycled_product_id': reproduct_search_ids[0].id,
                    'location_id': location_search,
                    'location_dest_id': location_dest_search,
                    'wash_date':date,
                    'product_qty': 1.0,
                    'product_uom': product_search_ids.uom_id.id,
                    'type_of_drum' :  product_search_ids.type_of_drum,
                    'state': 'draft',
                    'lot_id': int(barcode),
		
                }
                create_wash_order = self.env['wash.order'].create(wash_data)
                if create_wash_order:
                    return {'success': "Successfully Created Wash Order!"}



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
        internal_product_list = []
        location_list = []
        barcode_list = []
        used_barcode_list = []
        unused_barcode_list = []
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
            internal_product_list.append({'name': set_product_name or '',
                                          'id': str(data.id) or '',
                                          'default_code': data.default_code or '',
                                          'recycled_product_id': data.recycled_product_id.id or ''
                                          })

        rec_product_ids = product_obj.search([('id', '=', ctx.get('product_id'))])
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
        #         location_ids = location_obj.search([('usage', 'not in', ['supplier', 'production', 'view'])])
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
                'internal_product_list': internal_product_list,
                'barcode_list': barcode_selection,
                'location_list': location_list,
                'set_product_list': product_list,
                'set_barcode_list': barcode_list,
                'used_set_barcode_list': used_barcode_list,
                'unused_barcode_list': unused_barcode_list,
                'set_unused_barcode_list': set_unused_barcode_list,
                'type_of_order': [{'order': 'Container'}, {'order': 'Drum'}],
                # 'recycled_product' : recycled_product,
            }
            user_id[0].update(data)
            return user_id
        else:
            raise UserError(_('Login User Is Not Set As Employee!'))

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

    '''@api.multi
    def get_repair_part(self, ):
        product_obj = self.env['product.product']
        product_list = []
        repait_container_parts_ids = self.env.ref('ballester_wash.product_param_5_id')
        part_id = int(repait_container_parts_ids.value)
        product_ids = product_obj.search([('sale_ok', '=', True), ('type', '=', 'product'),('categ_id','=' ,part_id)])
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
                                 })
        product_selection = ''
        if len(product_list) > 0:
            product_selection = '<select class="products" style="overflow-y: auto!important; font-size: 18px;">'
            for line in product_list:
                product_selection += '<option label="' + line['default_code'] + '" ids="' + line[
                    'id'] + '"' + ' value="' + line['name'] + '">' + line[
                                         'name'] + '</option>'
            product_selection += '</select>'
        else:
            product_selection = '<select class="products" style="overflow-y: auto!important; font-size: 18px;"><option> No Data Found !</option> </select>'
        data = {
                'product_list': product_selection,}
        return data'''



    @api.multi
    def create_repair(self, wash_order):
        if wash_order:
            reapir_data = []
            wash_brw = self.env['wash.order'].browse(wash_order)
            repair_vals = {
			'wash_id':wash_order,
			'name' : self.env['ir.sequence'].next_by_code('mrp.repair'),
                        'product_id': wash_brw.product_id.id,
			'product_qty': wash_brw.product_qty,
			'product_uom': wash_brw.product_uom.id,
			'location_id':  wash_brw.location_id.id,
                        'location_dest_id' : wash_brw.location_dest_id.id,
			'lot_id': wash_brw.lot_id.id,
			'invoice_method':  'none',
			#'operations': wash_brw.operations,
			}
            repair_obj = self.env['mrp.repair']
            repair_id = repair_obj.create(repair_vals)
            wash_brw.state = 'repair_create'
            repair_id.state = 'confirmed'
            dangerous_characteristics = []
            variants =[]
            if repair_id.wash_id.product_id.danger_char_ids:
                for char in repair_id.wash_id.product_id.danger_char_ids:
                    dangerous_characteristics.append(char.description)
            if repair_id.wash_id.product_id.attribute_value_ids:
                for attr in repair_id.wash_id.product_id.attribute_value_ids:
                    variants.append(attr.name)
            reapir_data.append({
		'wash_order': repair_id.wash_id.name,
		'repair_order':  repair_id.name,
		'product_id': repair_id.product_id.name,
		'barcode': repair_id.lot_id.name,
		'ler':repair_id.wash_id.product_id.lercode_id.name or '',
		'un_code':repair_id.product_id.uncode or '', 
		'img_url': repair_id.product_id.image,
		'repair_state': repair_id.state,
		'dangerous_characteristics':dangerous_characteristics,
		'variants':variants,
		
				})
            return {'success': _('Successfully Created the Barcode!'), 'repair_data': reapir_data}

    @api.multi
    def create_repair_screen(self, number_of_barcode):
        if number_of_barcode:
            reapir_data = []
            wash_order_data =[]
            number = int(number_of_barcode)
            search_lot_ids = self.env['stock.production.lot'].search([('name','=',number)])
            if search_lot_ids:
                wash_brw = self.env['wash.order'].search([('lot_id','=',search_lot_ids[0].id)])
                if wash_brw:
                    dangerous_characteristics = []
                    variants =[]
                    recycled_product_name = False
                    if wash_brw[0].recycled_product_id:
                        recycled_product_name = wash_brw[0].recycled_product_id.name
                    if wash_brw[0].product_id.danger_char_ids:
                        for char in wash_brw[0].product_id.danger_char_ids:
                            dangerous_characteristics.append(char.description)
                    if wash_brw[0].product_id.attribute_value_ids:
                        for attr in wash_brw[0].product_id.attribute_value_ids:
                            variants.append(attr.name)
                    repair_vals = {
			'wash_id':wash_brw[0].id,
			'name' : self.env['ir.sequence'].next_by_code('mrp.repair'),
                        'product_id': wash_brw[0].product_id.id,
			'product_qty': wash_brw[0].product_qty,
			'product_uom': wash_brw[0].product_uom.id,
			'location_id':  wash_brw[0].location_id.id,
                        'location_dest_id' : wash_brw[0].location_dest_id.id,
			'lot_id': wash_brw[0].lot_id.id,
			'invoice_method':  'none',
			}
                    repair_obj = self.env['mrp.repair']
                    repair_id = repair_obj.create(repair_vals)
                    wash_brw[0].state = 'repair_create'
                    repair_id.state = 'confirmed'
                    reapir_data.append({
				'wash_id':wash_brw[0].id,
				'wash_order': repair_id.wash_id.name,
				'repair_order':  repair_id.name,
				'product_id': repair_id.product_id.name,
				'barcode': repair_id.lot_id.name,
				'ler':repair_id.wash_id.product_id.lercode_id.name or '',
				'un_code':repair_id.product_id.uncode or '', 
				'img_url': repair_id.product_id.image,
				'repair_state': repair_id.state,
				'dangerous_characteristics':dangerous_characteristics,
				'variants':variants,
		
				})
                    wash_order_data.append({
			'barcode': wash_brw[0].lot_id.name,
                        'img_url': wash_brw[0].product_id.image,
                         'order_number': wash_brw[0].name,
			   'type_of_order':wash_brw[0].type_of_order,
			   'dangerous_characteristics': dangerous_characteristics,
		           'state':wash_brw[0].state,
			  'ler': wash_brw[0].product_id.lercode_id.name or '',
			'un_code': wash_brw[0].product_id.uncode or '',
			'variants':variants,
			'recycled_product' : recycled_product_name,
			'location_id':wash_brw[0].location_id.name,
			'dest_location_id': wash_brw[0].location_dest_id.name,
			'repair_order' :wash_brw[0].name,
			'wash_id': wash_brw[0].id,
				})
                    return {'success': _('Successfully Created the Barcode!'), 'repair_data': reapir_data,'wash_order_data':wash_order_data}


    @api.multi
    def start_repair(self, repair_order):
        if repair_order:
            user_tz = self.env.user.tz
            local = pytz.timezone(user_tz)
            start_date = datetime.today()
            p_time = fields.Datetime.now(local)
            reapir_data = []
            repair_brw = self.env['mrp.repair'].search([('name','=', repair_order )])
            repair_brw.write({'state':'under_repair', 'start_datetime' : p_time})
            return {'success': _('Successfully started')}

    @api.multi
    def transfer_to_storewash(self, number_of_barcode,transfer_location_id, emp):
        location_obj = self.env['stock.location']
        if number_of_barcode:
            number = int(number_of_barcode) 
            inventory_obj = self.env['stock.inventory']
            user_tz = self.env.user.tz
            local = pytz.timezone(user_tz)
            start_date = datetime.today()
            p_time = fields.Datetime.now(local)
            account_id = self.env.ref('ballester_wash.analytic_account_wash_id', False).id
            emp_id =False
            emp_id = self.env['hr.employee'].search([('user_id','=', self._uid)])
            if emp_id:
                emp_id = emp_id[0].id
            if emp != None:
                emp_id = emp
            search_lot_ids = self.env['stock.production.lot'].search([('name','=',number)])
            if search_lot_ids:
                move_line_data =[]
                product_data = []
                location_search = False
                
                search_wash_order = self.env['wash.order'].search([('type_of_order','=','container'),('lot_id','=',search_lot_ids[0].id )])
                search_drum_wash_order = self.env['wash.order'].search([('type_of_order','=','drum'),('lot_id','=',search_lot_ids[0].id )])
                if search_drum_wash_order:
   
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(search_drum_wash_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')
                
                    m , s = divmod(pausetime_diff.total_seconds(), 60)
                    h, m = divmod(m, 60)
                    dur_h = (_('%0*d') % (2, h))
                    dur_m = (_('%0*d') % (2, m * 1.677966102))
                    dur_s = (_('%0*d') % (2, s))
                    duration = dur_h + '.' + dur_m + '.' + dur_s
                    hr_duration = dur_h + '.' + dur_m 
                    amount = float(hr_duration)
                    timesheet_vals ={
			'name': 'drying to Transter store time',
                        'date': start_date,
			 'amount': amount,
			'account_id':account_id ,
                         'employee_id':emp_id ,
                        'time': duration,
                         
				}
                    search_drum_wash_order[0].write({'state' : 'transfer_to_store','timesheet_ids': [(0,0, timesheet_vals)] ,'end_wash_datetime' : p_time})
                    warehouse_search = self.env['stock.warehouse'].search([('code','=','A1')])
                    if search_drum_wash_order[0].recycled_product_id:
                        if transfer_location_id:
                            first_location_name = transfer_location_id.split('/')
                            if len(first_location_name) >= 3:
                                parent_location_search =  location_obj.search([('name','=' ,first_location_name[0])])
                                prent_of_parent_search = location_obj.search([('location_id','=' ,parent_location_search[0].id)])
                                location_search = location_obj.search([('name','=' ,first_location_name[2]), ('location_id','=', prent_of_parent_search[0].id)])
                            else:
                                parent_location_search =  location_obj.search([('name','=' ,first_location_name[0])])
                                location_search = location_obj.search([('name','=' ,first_location_name[-1]), ('location_id','=', parent_location_search[0].id)])
                            if location_search:
                                location_search = location_search[0].id
                        pro_line_values = {  
                                    'product_id' :search_drum_wash_order[0].product_id.id,
                                    'product_uom_id' :search_drum_wash_order[0].product_id.uom_id.id,
                                    'prod_lot_id' :search_drum_wash_order[0].lot_id.id,
                                    'product_qty' :0,
                                    'location_id' :search_drum_wash_order[0].location_id.id,
                                    'state':'confirm'
                                    }
                        pro_inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
                        pro_inv_vals = {'name' :pro_inventory_sequence,
                           'filter':'product',
                           'line_ids': [(0, 0,  pro_line_values)],
                           'location_id' :search_drum_wash_order[0].location_id.id,
                           'product_id': search_drum_wash_order[0].product_id.id,
                           'wash_id': search_drum_wash_order[0].id
                            }
                        pro_inv = inventory_obj.create(pro_inv_vals)
                        pro_inv.action_start()
                        pro_inv.action_done()
                        ###recycled product inventory
                        #lot_create_id = self.env['stock.production.lot'].create({'product_id': search_drum_wash_order[0].recycled_product_id.id,'product_uom_id': search_drum_wash_order[0].recycled_product_id.uom_id.id ,'name':self.env['ir.sequence'].next_by_code('ballester.stock.production.lot')})
                        line_values = {  
                                    'product_id' :search_drum_wash_order[0].recycled_product_id.id,
                                    'product_uom_id' :search_drum_wash_order[0].recycled_product_id.uom_id.id,
                                    'prod_lot_id' :search_drum_wash_order[0].lot_id.id,
                                    'product_qty' : 1,
                                    'location_id' :location_search,
                                    'state':'confirm'
                                    }
                        inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
                        inv_vals = {'name' :inventory_sequence,
                           'filter':'product',
                           'line_ids': [(0, 0,  line_values)],
                           'location_id' :location_search,
                           'product_id': search_drum_wash_order[0].recycled_product_id.id,
                           'wash_id': search_drum_wash_order[0].id
                            }
                        pro_inv = inventory_obj.create(inv_vals)
                        pro_inv.action_start()
                        pro_inv.action_done()
                    return {'success': _('Successfully started')}
                if search_wash_order:
                  
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(search_wash_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')
                
                    m , s = divmod(pausetime_diff.total_seconds(), 60)
                    h, m = divmod(m, 60)
                    dur_h = (_('%0*d') % (2, h))
                    dur_m = (_('%0*d') % (2, m * 1.677966102))
                    dur_s = (_('%0*d') % (2, s))
                    duration = dur_h + '.' + dur_m + '.' + dur_s
                    hr_duration = dur_h + '.' + dur_m 
                    amount = float(hr_duration)
                    timesheet_vals ={
			'name': 'drying to Transter store time',
                        'date': start_date,
			 'amount': amount,
			'account_id':account_id ,
                         'employee_id':emp_id ,
                        'time': duration,
                         
				}
                    search_wash_order[0].write({'state' : 'transfer_to_store','timesheet_ids': [(0,0, timesheet_vals)] ,'end_wash_datetime' : p_time})
                
                    if search_wash_order[0].recycled_product_id:
                        if transfer_location_id:
                            first_location_name = transfer_location_id.split('/')
                            if len(first_location_name) >= 3:
                                parent_location_search =  location_obj.search([('name','=' ,first_location_name[0])])
                                prent_of_parent_search = location_obj.search([('location_id','=' ,parent_location_search[0].id)])
                                location_search = location_obj.search([('name','=' ,first_location_name[2]), ('location_id','=', prent_of_parent_search[0].id)])
                            else:
                                parent_location_search =  location_obj.search([('name','=' ,first_location_name[0])])
                                location_search = location_obj.search([('name','=' ,first_location_name[-1]), ('location_id','=', parent_location_search[0].id)])
                        pro_line_values = {  
                                    'product_id' :search_wash_order[0].product_id.id,
                                    'product_uom_id' :search_wash_order[0].product_id.uom_id.id,
                                    'prod_lot_id' :search_wash_order[0].lot_id.id,
                                    'product_qty' :0,
                                    'location_id' :search_wash_order[0].location_id.id,
                                    'state':'confirm'
                                    }
                        pro_inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
                        pro_inv_vals = {'name' :pro_inventory_sequence,
                           'filter':'product',
                           'line_ids': [(0, 0,  pro_line_values)],
                           'location_id' :search_wash_order[0].location_id.id,
                           'product_id': search_wash_order[0].product_id.id,
                           'wash_id': search_wash_order[0].id
                            }
                        pro_inv = inventory_obj.create(pro_inv_vals)
                        pro_inv.action_start()
                        pro_inv.action_done()
                        ###recycled product inventory
                        #lot_create_id = self.env['stock.production.lot'].create({'product_id': search_wash_order[0].recycled_product_id.id,'product_uom_id': search_wash_order[0].recycled_product_id.uom_id.id ,'name':self.env['ir.sequence'].next_by_code('ballester.stock.production.lot')})
                        line_values = {  
                                    'product_id' :search_wash_order[0].recycled_product_id.id,
                                    'product_uom_id' :search_wash_order[0].recycled_product_id.uom_id.id,
                                    'prod_lot_id' :search_wash_order[0].lot_id.id,
                                    'product_qty' : 1,
                                    'location_id' :location_search[0].id,
                                    'state':'confirm'
                                    }
                        inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
                        inv_vals = {'name' :inventory_sequence,
                           'filter':'product',
                           'line_ids': [(0, 0,  line_values)],
                           'location_id' :location_search[0].id,
                           'product_id': search_wash_order[0].recycled_product_id.id,
                           'wash_id': search_wash_order[0].id
                            }
                        pro_inv = inventory_obj.create(inv_vals)
                        pro_inv.action_start()
                        pro_inv.action_done()
                    return {'success': _('Successfully started')}


    @api.multi
    def stop_repair(self, repair_order):
        if repair_order:
            user_tz = self.env.user.tz
            local = pytz.timezone(user_tz)
            start_date = datetime.today()
            p_time = fields.Datetime.now(local)
            inventory_obj = self.env['stock.inventory']
            reapir_data = []
            account_id = self.env.ref('ballester_wash.analytic_account_wash_id', False).id
            emp_id =False
            emp_id = self.env['hr.employee'].search([('user_id','=', self._uid)])
            if emp_id:
                emp_id = emp_id.id
            repair_brw = self.env['mrp.repair'].search([('name','=', str(repair_order))])
            if repair_brw:
                pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(repair_brw.start_datetime), '%Y-%m-%d %H:%M:%S')
                m , s = divmod(pausetime_diff.total_seconds(), 60)
                h, m = divmod(m, 60)
                dur_h = (_('%0*d') % (2, h))
                dur_m = (_('%0*d') % (2, m * 1.677966102))
                dur_s = (_('%0*d') % (2, s))
                duration = dur_h + '.' + dur_m + '.' + dur_s
                hr_duration = dur_h + '.' + dur_m 
                amount = float(hr_duration)
                timesheet_vals ={
		            'name': 'Repair Time',
		            'date': start_date,
		            'amount': amount,
		            'account_id':account_id ,
		            'employee_id':emp_id ,
		            'time': duration,
		        }
                repair_brw.write({'state' : 'done','timesheet_ids': [(0,0, timesheet_vals)] })
                return {'success': _('Successfully started')}

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
                return {'product_name':  display_name , 'lot_list':lot_list , 'pro_name' : product_search[0].name}
        else:
            return {}

    @api.multi
    def get_product_data(self, product):
        product_des = ''
        if product:
            product_name = product.split('] ')
            if len(product_name) == 2:
                product_des = product_name[1]
            else:
                product_des = product_name[0]
            product_search = self.env['product.product'].search([('name','=', product_des )])
            
            return {'success': _('Successfully started')}

    @api.multi
    def view_repair_data(self, number_of_barcode):
        uid = request.session.uid
        ctx = dict(self._context)
        lot_obj = self.env['stock.production.lot']
        location_obj = self.env['stock.location']
        product_obj = self.env['product.product']
        user_id = self.env['res.users'].sudo().search_read([('id', '=', uid)], limit=1)
        barcode = int(number_of_barcode)
        wash_order_data= []
        if barcode:
            search_lot_ids = self.env['stock.production.lot'].search([('name','=',barcode)])
            if search_lot_ids:
                search_wash_order_ids = self.env['wash.order'].search([('lot_id','=' ,search_lot_ids[0].id )])
                if search_wash_order_ids:
                    search_repair_order_ids = self.env['mrp.repair'].search([('wash_id','=' ,search_wash_order_ids[0].id )])
                    if search_repair_order_ids:
                        dangerous_characteristics = []
                        variants =[]
                        recycled_product_name = False
                        if search_wash_order_ids[0].recycled_product_id:
                            recycled_product_name = search_wash_order_ids[0].recycled_product_id.name
                        if search_wash_order_ids[0].product_id.danger_char_ids:
                           for char in search_wash_order_ids[0].product_id.danger_char_ids:
                               dangerous_characteristics.append(char.description)
                        if search_wash_order_ids[0].product_id.attribute_value_ids:
                           for attr in search_wash_order_ids[0].product_id.attribute_value_ids:
                               variants.append(attr.name)
                        wash_order_data.append({
			'barcode': search_wash_order_ids[0].lot_id.name,
                        'img_url': search_wash_order_ids[0].product_id.image,
                         'order_number': search_wash_order_ids[0].name,
			   'type_of_order':search_wash_order_ids[0].type_of_order,
			   'dangerous_characteristics': dangerous_characteristics,
		           'state':search_repair_order_ids[0].state,
			  'ler': search_wash_order_ids[0].product_id.lercode_id.name or '',
			'un_code': search_wash_order_ids[0].product_id.uncode or '',
			'variants':variants,
			'recycled_product' : recycled_product_name,
			'location_id':search_wash_order_ids[0].location_id.name,
			'dest_location_id': search_wash_order_ids[0].location_dest_id.name,
			'repair_order' :search_repair_order_ids[0].name,
			'wash_id': search_wash_order_ids[0].id,
				})
                        return {'repair_data': wash_order_data
				}
        

    @api.multi
    def get_repair_data(self):
        uid = request.session.uid
        ctx = dict(self._context)
        lot_obj = self.env['stock.production.lot']
        location_obj = self.env['stock.location']
        user_id = self.env['res.users'].sudo().search_read([('id', '=', uid)], limit=1)
        internal_product_list = []
        location_list = []
        barcode_list = []
        product_obj = self.env['product.product']
        product_list = []
        repair_container_parts_ids = self.env.ref('ballester_wash.product_param_5_id')
        repair_drum_parts_ids = self.env.ref('ballester_wash.product_param_6_id')
        part_id = int(repair_container_parts_ids.value)
        drum_part_id = int(repair_drum_parts_ids.value)
        if ctx.get('con_add_repair_parts'):
            product_ids = product_obj.search([('sale_ok', '=', True), ('type', '=', 'product'),('categ_id','=' ,part_id)])
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
                                 })
        if ctx.get('drum_add_repair_parts'):
            product_ids = product_obj.search([('sale_ok', '=', True), ('type', '=', 'product'),('categ_id','=' ,drum_part_id)])
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
                                 })
        product_selection = ''
        if len(product_list) > 0:
            product_selection = '<select class="products" style="overflow-y: auto!important; font-size: 18px;">'
            for line in product_list:
                product_selection += '<option label="' + line['default_code'] + '" ids="' + line[
                    'id'] + '"' + ' value="' + line['name'] + '">' + line[
                                         'name'] + '</option>'
            product_selection += '</select>'
        else:
            product_selection = '<select class="products" style="overflow-y: auto!important; font-size: 18px;"><option> No Data Found !</option> </select>'
        return {'success': (_('successfully')),
		'product_list': product_selection,
		#'barcode_list' : barcode_selection,
		#'location_list': location_selection,
		#'dest_location_list' : dest_location_selection
			}

    @api.multi
    def compliance_value(self, answer_set,survey_id,wash_order,emp_id, page_id ,questions):
        emp_email = False
        if answer_set:
            if emp_id:
                emp_obj = self.env['hr.employee']
                emp_brw = emp_obj.browse(emp_id)
                if emp_brw:
                    emp_email = emp_brw.work_email
            incidents_manager_id = False
            incidents_manager = False
            wash_order_brw = self.env['wash.order'].browse(wash_order)
            user_id = self.env.uid
            search_emp_id = request.env['hr.employee'].search([('user_id','=',user_id )])
            return_result = []
            user_tz = self.env.user.tz
            local = pytz.timezone(user_tz)
            date = datetime.now(local)
            for label in answer_set:
                search_label_ids = self.env['survey.label'].search([('value','=', str(label['value'])),('question_id','=', int(label['question_id']))])
                survey_input_line_value= {
		'page_id': page_id,
		'survey_id':survey_id,
		'question_id': int(label['question_id']),
		'answer_type':'suggestion',
		'employee_id':emp_id,
		'value_suggested': search_label_ids[0].id,
					}
                survey_input_vals = {
                 'user_input_line_ids': [(0,0,survey_input_line_value)],
		'survey_id': survey_id,
		'date_create': date,
                'type': 'manually',
		'state':'done',
		'employee_id': emp_id,
		'email': emp_email,
		'wash_order_id':int(wash_order),
			}
            
                survey_input = self.env['survey.user_input'].create(survey_input_vals)
            
                if search_label_ids:
                    if search_label_ids[0].execution_type == 'send_mail':
                        incidents_manager_id = search_label_ids[0].controller_id.id 
                        incidents_manager = search_label_ids[0].controller_id.user_id.partner_id.id
                        if incidents_manager:
                            partner_ids = [incidents_manager]
                        elif search_emp_id.incidents_manager_id:
                            partner_ids =[ search_emp_id.incidents_manager_id.user_id.partner_id.id ]
                        if wash_order_brw.type_of_order == 'drum':
                            mail_val = {
	                          'subject':'Incident Created',
	                          'body': ('Incident Created BY %s .')%(self.env.user.name,),
	                          'author_id': self.env.user.partner_id.id,
	                           'email_from': self.env.user.login ,
	                           'message_type':'email',
	                           'model':'wash.order',
	                           'partner_ids':[(6,0, partner_ids )] , 
	                           'res_id': wash_order_brw[0].id
	                            }
                            a = request.env['mail.message'].create(mail_val)
                            wash_order_write = wash_order_brw.write({'state' : 'end_wash'})
                            return_result.append("negative")
                        elif wash_order_brw.type_of_order == 'container':
                            mail_val = {
	                          'subject':'Incident Created',
	                          'body': ('Incident Created BY %s .')%(self.env.user.name,),
	                          'author_id': self.env.user.partner_id.id,
	                           'email_from': self.env.user.login ,
	                           'message_type':'email',
	                           'model':'wash.order',
	                           'partner_ids':[(6,0, partner_ids )] , 
	                           'res_id': wash_order_brw[0].id
	                            }
                        
                            wash_order_write = wash_order_brw.write({'state' : 'check_compliance'})
                            return_result.append("negative")
                    
                    elif search_label_ids[0].execution_type == 'continue':
                        wash_order_write = wash_order_brw.write({'state' : 'quality_control'})
                        return_result.append("positive")
            if 'negative' in return_result:
                return {'negative_success': (_("Survey Created"))}
            elif 'positive' in return_result:
                return {'success': (_("Survey Created"))}
            else:
                return {'negative_success': (_("Survey Created"))}
        else:
            return {'warning': 'No answer submitted'}
    

    @api.multi
    def compliance_repair_value(self,answer_set,survey_id,repair_order,emp_id, page_id ,questions):
        emp_email = False
        if emp_id:
            emp_obj = self.env['hr.employee']
            emp_brw = emp_obj.browse(emp_id)
            if emp_brw:
                emp_email = emp_brw.work_email
        incidents_manager_id = False
        incidents_manager = False
        repair_order_brw = self.env['mrp.repair'].search([('name','=', repair_order)])
        user_id = self.env.uid
        search_emp_id = request.env['hr.employee'].search([('user_id','=',user_id )])
        return_result = []
        user_tz = self.env.user.tz
        local = pytz.timezone(user_tz)
        date = datetime.now(local)
        if answer_set:
            for label in answer_set:
                search_label_ids = self.env['survey.label'].search([('value','=', str(label['value'])),('question_id','=',int(label['question_id']))])
                survey_input_line_value= {
		'page_id': page_id,
		'survey_id':survey_id,
		'question_id': int(label['question_id']),
		'answer_type':'suggestion',
		'employee_id':emp_id,
		'value_suggested': search_label_ids[0].id,
					}
                survey_input_vals = {
                 'user_input_line_ids': [(0,0,survey_input_line_value)],
		'survey_id': survey_id,
		'date_create': date,
                'type': 'manually',
		'employee_id': emp_id,
		'state':'done',
		'email': emp_email,
			}
                survey_input = self.env['survey.user_input'].create(survey_input_vals)
                if search_label_ids:
                    if search_label_ids[0].execution_type == 'send_mail':
                        incidents_manager_id = search_label_ids[0].controller_id.id 
                        incidents_manager = search_label_ids[0].controller_id.user_id.partner_id.id
                        if incidents_manager:
                            partner_ids = [incidents_manager]
                        elif search_emp_id.incidents_manager_id:
                            partner_ids =[ search_emp_id.incidents_manager_id.user_id.partner_id.id ]
                        if repair_order_brw.type_of_order == 'drum':
                            mail_val = {
	                          'subject':'Incident Created',
	                          'body': ('Incident Created BY %s .')%(self.env.user.name,),
	                          'author_id': self.env.user.partner_id.id,
	                           'email_from': self.env.user.login ,
	                           'message_type':'email',
	                           'model':'mrp.repair',
	                           'partner_ids':[(6,0, partner_ids )] , 
	                           'res_id': repair_order_brw[0].id
	                            }
                            a = request.env['mail.message'].create(mail_val)
                            repair_order_write = repair_order_brw.write({'state' : 'end_wash'})
                            return_result.append("negative")
                    elif search_label_ids[0].execution_type == 'continue':
                        repair_order_write = repair_order_brw.write({'state' : 'check_compliance'})
                        return_result.append("positive")
            if 'negative' in return_result:
                return {'negative_success': (_("Survey Created"))}
            elif 'positive' in return_result:
                return {'success': (_("Survey Created"))}
            else:
                return {'negative_success': (_("Survey Created"))}
        else:
            return {'warning': 'No answer submitted'}

    @api.multi
    def check_compliance(self, number_of_barcode):
        context = self._context
        survey_container = False
        survey_drum = False
        survey_crush = False
        survey_compact = False
        survey_obj = self.env['survey.survey']
        emp_id =False
        user = self.env.user
        lang = user.lang
        emp_id = self.env['hr.employee'].search([('user_id','=', self._uid)])
        if emp_id:
            emp_id = emp_id.id
        if number_of_barcode == '':
            return {'warning': 'Please first scan Barcode!'}
        if number_of_barcode:
            number = int(number_of_barcode)
            search_lot_ids = self.env['stock.production.lot'].search([('name','=',number)])
            if search_lot_ids:
                wash_order_data = []
                search_wash_order = self.env['wash.order'].search([('type_of_order','=','container'),('lot_id','=',search_lot_ids[0].id )])
                
                search_drum_wash_order = self.env['wash.order'].search([('type_of_order','=','drum'),('lot_id','=',search_lot_ids[0].id )])
                if search_drum_wash_order and context.get('compliance_wash_order'):
                    dangerous_characteristics = []
                    variants =[]
                    recycled_product_name = False
                    if search_drum_wash_order[0].recycled_product_id:
                        recycled_product_name = search_drum_wash_order[0].recycled_product_id.name
                    if search_drum_wash_order[0].product_id.danger_char_ids:
                        for char in search_drum_wash_order[0].product_id.danger_char_ids:
                           dangerous_characteristics.append(char.description)
                    if search_drum_wash_order[0].product_id.attribute_value_ids:
                        for attr in search_drum_wash_order[0].product_id.attribute_value_ids:
                           variants.append(attr.name)
                    wash_order_data.append({
			'barcode': search_drum_wash_order[0].lot_id.name,
                        'img_url': search_drum_wash_order[0].product_id.image,
                         'order_number': search_drum_wash_order[0].name,
			   'type_of_order':search_drum_wash_order[0].type_of_order,
			   'dangerous_characteristics': dangerous_characteristics,
		           'state':search_drum_wash_order[0].state,
			  'ler': search_drum_wash_order[0].product_id.lercode_id.name or '',
			'un_code': search_drum_wash_order[0].product_id.uncode or '',
			'variants':variants,
			'recycled_product' : recycled_product_name,
			'location_id':search_drum_wash_order[0].location_id.name,
			'dest_location_id': search_drum_wash_order[0].location_dest_id.name,
				})
                    survey_drum = self.env['ir.config_parameter'].sudo().get_param('drum_compliance_id')
                    if survey_drum:
                        survey_drum_id = survey_obj.search([('id', '=', survey_drum)])
                  
                        if  survey_drum_id:
			    
                            if survey_drum_id.page_ids:
                                
                                for page in survey_drum_id.page_ids:
                                    question_set = []
                                    page_id = page.id
                                    if page.question_ids:
                                        
                                        for question in page.question_ids:
                                            question_id = question.id
                                            question_choice_set = []
                                            for label in question.labels_ids:
                                                question_choice_set.append({'answer': label.value,
								'answer_id' : label.id,
								'execution_type':label.execution_type or ''
									})
                                            question_set.append({
						'question' :question.with_context(lang=lang).question,
						'choice': question_choice_set,
						'question_id': question_id, 
							})
                                    else:
                                        return {'warning': "no questions"}                       

                                    return {'success': (_('successufully')) ,'emp_id':emp_id, 'page_id':page_id, 'question_id': question_id,  'question_set' :question_set,'survey_id':survey_drum_id[0].id, 'wash_order': search_drum_wash_order[0].id ,'wash_order_data':wash_order_data }
                if search_wash_order and context.get('compliance_wash_order'):
                    dangerous_characteristics = []
                    variants =[]
                     
                    recycled_product_name = False
                    if search_wash_order[0].recycled_product_id:
                        recycled_product_name = search_wash_order[0].recycled_product_id.name
                    if search_wash_order[0].product_id.danger_char_ids:
                        for char in search_wash_order[0].product_id.danger_char_ids:
                           dangerous_characteristics.append(char.description)
                    if search_wash_order[0].product_id.attribute_value_ids:
                        for attr in search_wash_order[0].product_id.attribute_value_ids:
                           variants.append(attr.name)
                    wash_order_data.append({
			'barcode': search_wash_order[0].lot_id.name,
                        'img_url': search_wash_order[0].product_id.image,
                         'order_number': search_wash_order[0].name,
			   'type_of_order':search_wash_order[0].type_of_order,
			   'dangerous_characteristics': dangerous_characteristics,
		           'state':search_wash_order[0].state,
			  'ler': search_wash_order[0].product_id.lercode_id.name or '',
			'un_code': search_wash_order[0].product_id.uncode or '',
			'variants':variants,
			'recycled_product' : recycled_product_name,
			'location_id':search_wash_order[0].location_id.name,
			'dest_location_id': search_wash_order[0].location_dest_id.name,
				})
                    survey_container = self.env['ir.config_parameter'].sudo().get_param('container_compliance_id') 
                    if survey_container:
                        survey_container_id = survey_obj.search([('id', '=', survey_container)])
                        if  survey_container_id:
			    
                            if survey_container_id.page_ids:
                                
                                for page in survey_container_id.page_ids:
                                    question_set = []
                                    page_id = page.id
                                    if page.question_ids:
                                        
                                        for question in page.question_ids:
                                            question_id = question.id
                                            question_choice_set = []
                                            for label in question.labels_ids:
                                                question_choice_set.append({'answer': label.value,
								'answer_id' : label.id,
								'execution_type':label.execution_type or ''
									})
                                            question_set.append({
						'question' :question.with_context(lang=lang).question,
						'choice': question_choice_set,
						'question_id': question_id, 
							})
                                    else:
                                        return {'warning': "no questions"}
                                    return {'success': (_('successufully')) ,'emp_id':emp_id, 'page_id':page_id, 'question_id': question_id,  'question_set' :question_set,'survey_id':survey_container_id[0].id, 'wash_order': search_wash_order[0].id ,'wash_order_data':wash_order_data }



    @api.multi
    def check_repair_compliance(self, repair_order):
        context = self._context
        survey_container = False
        survey_drum = False
        survey_crush = False
        survey_compact = False
        survey_obj = self.env['survey.survey']
        emp_id =False
        user = self.env.user
        lang = user.lang
        emp_id = self.env['hr.employee'].search([('user_id','=', self._uid)])
        if emp_id:
            emp_id = emp_id.id
        if repair_order:
            search_repair_order = self.env['mrp.repair'].search([('name','=',repair_order)])
            if search_repair_order:
                dangerous_characteristics = []
                variants =[]
                recycled_product_name = False
                survey_repair =  self.env['ir.config_parameter'].sudo().get_param('repair_compliance_id') 
                if survey_repair:
                    repair_compliance_id = survey_obj.search([('id', '=', survey_repair)])
                    if  repair_compliance_id:
                        if repair_compliance_id.page_ids:
                            for page in repair_compliance_id.page_ids:
                                question_set = []
                                page_id = page.id
                                if page.question_ids:
                                    
                                    for question in page.question_ids:
                                        question_id = question.id
                                        question_choice_set = []
                                        for label in question.labels_ids:
                                            question_choice_set.append({'answer': label.value,
								'answer_id' : label.id,
								'execution_type':label.execution_type or ''
									})
                                        question_set.append({
						'question' :question.with_context(lang=lang).question,
						'choice': question_choice_set,
						'question_id': question_id, 
							})
                                    return {'success': (_('successufully')) ,'emp_id':emp_id, 'page_id':page_id, 'question_id': question_id,  'question_set' :question_set,'survey_id':repair_compliance_id[0].id, }
                                             
    @api.multi
    def display_order(self, wash_order):           
        location_obj = self.env['stock.location']
        transfer_location_list = []
        location_ids = location_obj.search([('usage', 'in', ['internal'])])
        account_id = self.env.ref('ballester_wash.analytic_account_wash_id', False).id
        for location in location_ids:
            orig_location = location
            name = location.name
            while location.location_id and location.usage != 'view':
                location = location.location_id
                if not name:
                    raise UserError(_('You have to set a name for this location.'))
                name = location.name + "/" + name
            transfer_location_list.append({'name': name or '',
                                  'id': str(orig_location.id) or '',
                                  })
        wash_obj = self.env['wash.order']
        if wash_order:
            wash_brw = wash_obj.browse(wash_order)
            if wash_brw:
                dangerous_characteristics = []
                variants =[]
                wash_order_data=[]
                recycled_product_name = False
                if wash_brw.recycled_product_id:
                    recycled_product_name = wash_brw.recycled_product_id.name
                if wash_brw.product_id.danger_char_ids:
                    for char in wash_brw.product_id.danger_char_ids:
                        dangerous_characteristics.append(char.description)
                if wash_brw.product_id.attribute_value_ids:
                    for attr in wash_brw[0].product_id.attribute_value_ids:
                        variants.append(attr.name)
                product_img_url = wash_brw.product_id.image
                wash_order_data.append({'order_number': wash_brw.name,
					   'type_of_order':wash_brw.type_of_order,
					   'dangerous_characteristics': dangerous_characteristics,
                                           'state':wash_brw.state,
					  'ler': wash_brw.product_id.lercode_id.name or '',
						'un_code': wash_brw.product_id.uncode or '',
						'variants':variants,
						'recycled_product' : recycled_product_name,
						'lot_name' : wash_brw.lot_id.name,
						'location_id':  wash_brw.location_id.name,
						'dest_location_id':   wash_brw.location_dest_id.name,
						'transfer_location':   transfer_location_list,
			
                                              })

                return {'success': _('Successfully Created the Barcode!'), 'wash_order_data': wash_order_data, 'product_img_url':product_img_url }
                        
        


    # valide/click barcode
    @api.multi
    def search_barcode(self, number_of_barcode,emp):
        context = self._context 
        recycled_product_list = [] 
        delivery_location_list = []
        user_tz = self.env.user.tz
        local = pytz.timezone(user_tz)
        start_date = datetime.today()
        p_time = fields.Datetime.now(local)
        survey_obj = self.env['survey.survey']
        product_obj = self.env['product.product']
        inventory_obj = self.env['stock.inventory']
        location_obj = self.env['stock.location']
        location_ids = location_obj.search([('usage', 'in', ['internal'])])
        account_id = self.env.ref('ballester_wash.analytic_account_wash_id', False).id
        for location in location_ids:
            orig_location = location
            name = location.name
            while location.location_id and location.usage != 'view':
                location = location.location_id
                if not name:
                    raise UserError(_('You have to set a name for this location.'))
                name = location.name + "/" + name
            delivery_location_list.append({'name': name or '',
                                  'id': str(orig_location.id) or '',
                                  })
        emp_id =False
        emp_id = self.env['hr.employee'].search([('user_id','=', self._uid)])
        if emp_id:
            emp_id = emp_id[0].id
        if emp != None:
            emp_id =emp
        if number_of_barcode == '':
            return {'warning': 'Please first scan Barcode!'}
        if number_of_barcode:
            number_str = number_of_barcode.strip(" ")
            number_str1 = number_str.strip("\t")
            if len(number_str1) > 13:
                raise UserError(_('Wrong Barcode!!'))
            number = int(number_of_barcode)
            
            search_lot_ids = self.env['stock.production.lot'].search([('name','=',number)])
            '''product_ids = product_obj.search([('sale_ok', '=', True), ('type', '=', 'product')])
            for data in product_ids:
                set_product = self.set_product_name(data)
                set_product_name = ''
                if "''" in set_product:
                    set_product_name = set_product.replace("''", "*")
                else:
                    set_product_name = set_product.replace('"', "*")
                recycled_product_list.append({'name': set_product_name or '',
                                 'id': str(data.id) or '',
                                 'default_code': data.default_code or '',
                                 })'''
            if search_lot_ids:
                recycle_product_ids = self.env.ref('ballester_wash.product_param_7_id')
                re_product_id = int(recycle_product_ids.value)
                product_ids = product_obj.search([('sale_ok', '=', True), ('type', '=', 'product'),('categ_id','=',re_product_id )])
                if product_ids:
                    for data in product_ids:
                        set_product = self.set_product_name(data)
                        set_product_name = ''
                        if "''" in set_product:
                            set_product_name = set_product.replace("''", "*")
                        else:
                            set_product_name = set_product.replace('"', "*")
                        recycled_product_list.append({'name': set_product_name or '',
				                 'id': str(data.id) or '',
				                 'default_code': data.default_code or '',
				                 })
                search_wash_order = self.env['wash.order'].search([('type_of_order','=','container'),('lot_id','=',search_lot_ids[0].id )])
                search_drum_wash_order = self.env['wash.order'].search([('type_of_order','=','drum'),('lot_id','=',search_lot_ids[0].id )])
                search_crush_order= self.env['wash.order'].search([('type_of_order','=','crush'),('lot_id','=',search_lot_ids[0].id ),('state','in',['start_crush','stop_crush','draft'])])
                search_compact_order= self.env['wash.order'].search([('type_of_order','=','compact'),('lot_id','=',search_lot_ids[0].id ),('state','in',['start_crush','stop_crush','draft'])])
                search_drum_container_order= self.env['wash.order'].search([('type_of_order','in',['container','drum']),('lot_id','=',search_lot_ids[0].id ),('state','=','destructed')])
                if search_wash_order and context.get('display_barcode_details'):
                    dangerous_characteristics = []
                    wash_order_data = []
                    variants =[]
                    recycled_product_name = False
                    if search_wash_order[0].recycled_product_id:
                        recycled_product_name = search_wash_order[0].recycled_product_id.name
                    if search_wash_order[0].product_id.danger_char_ids:
                        for char in search_wash_order[0].product_id.danger_char_ids:
                           dangerous_characteristics.append(char.description)
                    if search_wash_order[0].product_id.attribute_value_ids:
                        for attr in search_wash_order[0].product_id.attribute_value_ids:
                           variants.append(attr.name)
                    product_img_url = search_wash_order[0].product_id.image
                    wash_order_data.append({'order_number': search_wash_order[0].name,
					   'type_of_order':search_wash_order[0].type_of_order,
					   'dangerous_characteristics': dangerous_characteristics,
                                           'state':search_wash_order[0].state,
					  'ler': search_wash_order[0].product_id.lercode_id.name or '',
						'un_code': search_wash_order[0].product_id.uncode or '',
						'variants':variants,
						'recycled_product' : recycled_product_name
                                              })

                    return {'success': _('Successfully Created the Barcode!'), 'wash_order_data': wash_order_data, 'product_img_url':product_img_url }
                elif search_drum_wash_order and context.get('drum_crush'):
                    if search_drum_wash_order[0].product_id.type_of_drum:
                        if search_drum_wash_order[0].product_id.type_of_drum == 'metal':
                            return {'warning_crush' : _('No crush order for Metal drum!')}
                        elif search_drum_wash_order[0].product_id.type_of_drum == 'plastic':
                            dangerous_characteristics = []
                            variants =[]
                            wash_order_data =[]
                            recycled_product_name = False
                            if search_drum_wash_order[0].recycled_product_id:
                                recycled_product_name = search_drum_wash_order[0].recycled_product_id.name
                            if search_drum_wash_order[0].product_id.danger_char_ids:
                                for char in search_drum_wash_order[0].product_id.danger_char_ids:
                                    dangerous_characteristics.append(char.description)
                            if search_drum_wash_order[0].product_id.attribute_value_ids:
                                for attr in search_drum_wash_order[0].product_id.attribute_value_ids:
                                    variants.append(attr.name)
                            if search_crush_order[0].state == 'draft':
                                wash_order_data.append({'order_number': search_crush_order[0].name,
					   'type_of_order':search_drum_wash_order[0].type_of_order,
					   'dangerous_characteristics': dangerous_characteristics,
					 'img_url': search_drum_wash_order[0].product_id.image,
                                           'state':search_crush_order[0].state,
					  'ler': search_drum_wash_order[0].product_id.lercode_id.name or '',
						'un_code': search_drum_wash_order[0].product_id.uncode or '',
						'variants':variants,
						'recycled_product' : recycled_product_list,
						'delivery_location': delivery_location_list,
						'barcode': search_drum_wash_order[0].lot_id.name,
                                              })
                                return {'success':'success creates','wash_order_data':wash_order_data,'product_img_url': search_drum_wash_order[0].product_id.image}
                elif search_drum_wash_order and context.get('drum_compact'):
                    if search_drum_wash_order[0].product_id.type_of_drum:
                        if search_drum_wash_order[0].product_id.type_of_drum == 'plastic':
                            return {'warning_compact' : _('No Compact order for Plastic drum!')}
                        elif search_drum_wash_order[0].product_id.type_of_drum == 'metal':
                            dangerous_characteristics = []
                            variants =[]
                            wash_order_data =[]
                            recycled_product_name = False
                            if search_drum_wash_order[0].recycled_product_id:
                                recycled_product_name = search_drum_wash_order[0].recycled_product_id.name
                            if search_drum_wash_order[0].product_id.danger_char_ids:
                                for char in search_drum_wash_order[0].product_id.danger_char_ids:
                                    dangerous_characteristics.append(char.description)
                            if search_drum_wash_order[0].product_id.attribute_value_ids:
                                for attr in search_drum_wash_order[0].product_id.attribute_value_ids:
                                    variants.append(attr.name)
                            product_img_url = search_drum_wash_order[0].product_id.image
                            if search_crush_order[0].state == 'draft':
                                wash_order_data.append({'order_number': search_crush_order[0].name,
					   'type_of_order':search_drum_wash_order[0].type_of_order,
					 'img_url': search_drum_wash_order[0].product_id.image,
					   'dangerous_characteristics': dangerous_characteristics,
                                           'state':search_crush_order[0].state,
					  'ler': search_drum_wash_order[0].product_id.lercode_id.name or '',
						'un_code': search_drum_wash_order[0].product_id.uncode or '',
						'variants':variants,
						'recycled_product' : search_crush_order[0].recycled_product_id.id,
						'delivery_location': search_crush_order[0].location_dest_id.id,
						'barcode': search_drum_wash_order[0].lot_id.name,
                                              })
                                return {'success':'success creates','wash_order_data':wash_order_data,'product_img_url': search_drum_wash_order[0].product_id.image}
                elif search_drum_wash_order and context.get('display_barcode_details'):
                    dangerous_characteristics = []
                    wash_order_data = []
                    variants =[]
                    recycled_product_name = False
                    if search_drum_wash_order[0].recycled_product_id:
                        recycled_product_name = search_drum_wash_order[0].recycled_product_id.name
                    if search_drum_wash_order[0].product_id.danger_char_ids:
                        for char in search_drum_wash_order[0].product_id.danger_char_ids:
                           dangerous_characteristics.append(char.description)
                    if search_drum_wash_order[0].product_id.attribute_value_ids:
                        for attr in search_drum_wash_order[0].product_id.attribute_value_ids:
                           variants.append(attr.name)
                    product_img_url = search_drum_wash_order[0].product_id.image
                    wash_order_data.append({'order_number': search_drum_wash_order[0].name,
					   'type_of_order':search_drum_wash_order[0].type_of_order,
					   'dangerous_characteristics': dangerous_characteristics,
                                           'state':search_drum_wash_order[0].state,
					  'ler': search_drum_wash_order[0].product_id.lercode_id.name or '',
						'un_code': search_drum_wash_order[0].product_id.uncode or '',
						'variants':variants,
						'recycled_product' : recycled_product_name,
                                              })

                    return {'success': _('Successfully Created the Barcode!'), 'wash_order_data': wash_order_data, 'product_img_url':product_img_url }
  
                elif search_drum_container_order and context.get('display_detail'):
                    dangerous_characteristics = []
                    variants =[]
                    wash_order_data=[]
                    recycled_product_name = False
                    if search_drum_container_order[0].recycled_product_id:
                        recycled_product_name = search_drum_container_order[0].recycled_product_id.name
                    if search_drum_container_order[0].product_id.danger_char_ids:
                        for char in search_drum_container_order[0].product_id.danger_char_ids:
                           dangerous_characteristics.append(char.description)
                    if search_drum_container_order[0].product_id.attribute_value_ids:
                        for attr in search_drum_container_order[0].product_id.attribute_value_ids:
                           variants.append(attr.name)
                    product_img_url = search_drum_container_order[0].product_id.image
                    wash_order_data.append({'order_number': search_drum_container_order[0].name,
					   'type_of_order':search_drum_container_order[0].type_of_order,
					   'dangerous_characteristics': dangerous_characteristics,
                                           'state':search_drum_container_order[0].state,
					      'ler': search_drum_container_order[0].product_id.lercode_id.name or '',
						'un_code': search_drum_container_order[0].product_id.uncode or '' ,
						'variants':variants,
						'recycled_product' : recycled_product_name
                                              })

                    return {'success': _('Successfully Created the Barcode!'), 'wash_order_data': wash_order_data, 'product_img_url':product_img_url }

                elif search_crush_order and context.get('crush_order'):
                    dangerous_characteristics = []
                    variants =[]
                    kilo_qty = 0.0
                    wash_order_data =[]
                    recycled_product_name = False
                    if search_crush_order[0].recycled_product_id:
                        recycled_product_name = search_crush_order[0].recycled_product_id.name
                    if search_crush_order[0].product_id.danger_char_ids:
                        for char in search_crush_order[0].product_id.danger_char_ids:
                           dangerous_characteristics.append(char.description)
                    if search_crush_order[0].product_id.attribute_value_ids:
                        for attr in search_crush_order[0].product_id.attribute_value_ids:
                           variants.append(attr.name)
                    product_img_url = search_crush_order[0].product_id.image
                    if search_crush_order[0].state == 'draft':
                        wash_order_data.append({'order_number': search_crush_order[0].name,
					       'type_of_order':search_crush_order[0].type_of_order,
					       'dangerous_characteristics': dangerous_characteristics,
                                               'state':search_crush_order[0].state,
					       'ler': search_crush_order[0].product_id.lercode_id.name or '',
						'un_code': search_crush_order[0].product_id.uncode or '',
						'variants':variants,
						'recycled_product' : recycled_product_list,
						'delivery_location': delivery_location_list,
						'barcode': search_crush_order[0].lot_id.name,
                                              })
                    elif search_crush_order[0].state in ['start_crush','stop_crush']:
                        wash_order_data.append({'order_number': search_crush_order[0].name,
						   'type_of_order':search_crush_order[0].type_of_order,
						   'dangerous_characteristics': dangerous_characteristics,
		                                   'state':search_crush_order[0].state,
						  'ler': search_crush_order[0].product_id.lercode_id.name or '',
						'un_code': search_crush_order[0].product_id.uncode or '',
						'variants':variants,
						'recycled_product' : search_crush_order[0].recycled_product_id.name,
						'delivery_location': search_crush_order[0].location_dest_id.name,
						'barcode': search_crush_order[0].lot_id.name,
						'kilo_qty': search_crush_order[0].product_id.plastic_kg,
                                              })
                    return {'wash_order_data': wash_order_data, 'product_img_url':product_img_url}
                elif search_compact_order and context.get('compact_order'):
                    dangerous_characteristics = []
                    kilo_qty = 0.0
                    variants =[]
                    wash_order_data =[]
                    recycled_product_name = False
                    if search_compact_order[0].recycled_product_id:
                        recycled_product_name = search_compact_order[0].recycled_product_id.name
                    if search_compact_order[0].product_id.danger_char_ids:
                        for char in search_compact_order[0].product_id.danger_char_ids:
                           dangerous_characteristics.append(char.description)
                    if search_compact_order[0].product_id.attribute_value_ids:
                        for attr in search_compact_order[0].product_id.attribute_value_ids:
                           variants.append(attr.name)
                    product_img_url = search_compact_order[0].product_id.image
                    if search_compact_order[0].state == 'draft':
                        wash_order_data.append({'order_number': search_compact_order[0].name,
					   'type_of_order':search_compact_order[0].type_of_order,
					   'dangerous_characteristics': dangerous_characteristics,
                                           'state':search_compact_order[0].state,
					  'ler': search_compact_order[0].product_id.lercode_id.name or '',
						'un_code': search_compact_order[0].product_id.uncode or '',
						'variants':variants,
						'recycled_product' : recycled_product_list,
						'delivery_location': delivery_location_list,
						'barcode': search_compact_order[0].lot_id.name,
                                              })
                    elif search_compact_order[0].state in ['start_crush','stop_crush']:
                        wash_order_data.append({'order_number': search_compact_order[0].name,
						   'type_of_order':search_compact_order[0].type_of_order,
						   'dangerous_characteristics': dangerous_characteristics,
		                                   'state':search_compact_order[0].state,
						  'ler': search_compact_order[0].product_id.lercode_id.name or '',
						'un_code': search_compact_order[0].product_id.uncode or '',
						'variants':variants,
						'recycled_product' : search_compact_order[0].recycled_product_id.name,
						'delivery_location': search_compact_order[0].location_dest_id.name,
						'barcode': search_compact_order[0].lot_id.name,
						'kilo_qty': search_compact_order[0].product_id.metal_kg,
                                              })
                    return {'wash_order_data': wash_order_data, 'product_img_url':product_img_url}
                elif search_drum_wash_order and context.get('display_drum_barcode_details'):
                    wash_order_data =[]
                    dangerous_characteristics = []
                    variants =[]
                    recycled_product_name = False
                    if search_drum_wash_order[0].recycled_product_id:
                        recycled_product_name = search_drum_wash_order[0].recycled_product_id.name
                    if search_drum_wash_order[0].product_id.danger_char_ids:
                        for char in search_drum_wash_order[0].product_id.danger_char_ids:
                           dangerous_characteristics.append(char.description)
                    if search_drum_wash_order[0].product_id.attribute_value_ids:
                        for attr in search_drum_wash_order[0].product_id.attribute_value_ids:
                           variants.append(attr.name)
                    product_img_url = search_drum_wash_order[0].product_id.image
                    wash_order_data.append({'order_number': search_drum_wash_order[0].name,
					   'type_of_order':search_drum_wash_order[0].type_of_order,
					   'dangerous_characteristics': dangerous_characteristics,
                                           'state':search_drum_wash_order[0].state,
					  'ler': search_drum_wash_order[0].product_id.lercode_id.name or '',
						'un_code': search_drum_wash_order[0].product_id.uncode or '',
						'variants':variants,
						'recycled_product' : recycled_product_name,
						'type_of_drum':search_drum_wash_order[0].type_of_drum,
                                              })

                    return {'success': _('Successfully Created the Barcode!'), 'wash_order_data': wash_order_data, 'product_img_url':product_img_url }

                elif search_drum_wash_order and context.get('start_drum_wash_order'):
                    dangerous_characteristics = []
                    variants =[]
                    recycled_product_name = False
                    if search_drum_wash_order[0].recycled_product_id:
                        recycled_product_name = search_drum_wash_order[0].recycled_product_id.name
                    if search_drum_wash_order[0].product_id.danger_char_ids:
                        for char in search_drum_wash_order[0].product_id.danger_char_ids:
                           dangerous_characteristics.append(char.description)
                    if search_drum_wash_order[0].product_id.attribute_value_ids:
                        for attr in search_drum_wash_order[0].product_id.attribute_value_ids:
                           variants.append(attr.name)
                    wash_order_data = []
                    search_drum_wash_order[0].write({'state':'start_wash', 'start_datetime': p_time }) 
                    wash_order_data.append({
			'barcode': search_drum_wash_order[0].lot_id.name,
                        'img_url': search_drum_wash_order[0].product_id.image,
                         'order_number': search_drum_wash_order[0].name,
			   'type_of_order':search_drum_wash_order[0].type_of_order,
			   'dangerous_characteristics': dangerous_characteristics,
		           'state':search_drum_wash_order[0].state,
			  'ler': search_drum_wash_order[0].product_id.lercode_id.name or '',
			'un_code': search_drum_wash_order[0].product_id.uncode or '',
			'variants':variants,
			'recycled_product' : recycled_product_name,
			'location_id':search_drum_wash_order[0].location_id.name,
			'dest_location_id': search_drum_wash_order[0].location_dest_id.name,
				})     
                    return {'success': _('Successfully Change Start Wash!'), 'wash_order_data':wash_order_data}
                elif search_drum_wash_order and context.get('end_drum_wash_order'):
                    dangerous_characteristics = []
                    variants =[]
                    wash_order_data = []
                    recycled_product_name = False
                    if search_drum_wash_order[0].recycled_product_id:
                        recycled_product_name = search_drum_wash_order[0].recycled_product_id.name
                    if search_drum_wash_order[0].product_id.danger_char_ids:
                        for char in search_drum_wash_order[0].product_id.danger_char_ids:
                           dangerous_characteristics.append(char.description)
                    if search_drum_wash_order[0].product_id.attribute_value_ids:
                        for attr in search_drum_wash_order[0].product_id.attribute_value_ids:
                           variants.append(attr.name)
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(search_drum_wash_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')
                    m , s = divmod(pausetime_diff.total_seconds(), 60)
                    h, m = divmod(m, 60)
                    dur_h = (_('%0*d') % (2, h))
                    dur_m = (_('%0*d') % (2, m * 1.677966102))
                    dur_s = (_('%0*d') % (2, s))
                    duration = dur_h + '.' + dur_m + '.' + dur_s
                    hr_duration = dur_h + '.' + dur_m 
                    amount = float(hr_duration)
                    timesheet_vals ={
			'name': 'Washing Time',
                        'date': start_date,
			 'amount': amount,
			'account_id':account_id ,
                         'employee_id':emp_id ,
                         'time': duration}
                    search_drum_wash_order[0].write({'state' : 'end_wash','timesheet_ids': [(0,0, timesheet_vals)] })
                    wash_order_data.append({
			'barcode': search_drum_wash_order[0].lot_id.name,
                        'img_url': search_drum_wash_order[0].product_id.image,
                         'order_number': search_drum_wash_order[0].name,
			   'type_of_order':search_drum_wash_order[0].type_of_order,
			   'dangerous_characteristics': dangerous_characteristics,
		           'state':search_drum_wash_order[0].state,
			  'ler': search_drum_wash_order[0].product_id.lercode_id.name or '',
			'un_code': search_drum_wash_order[0].product_id.uncode or '',
			'variants':variants,
			'recycled_product' : recycled_product_name,
			'location_id':search_drum_wash_order[0].location_id.name,
			'dest_location_id': search_drum_wash_order[0].location_dest_id.name,
				})   
                    return {'success': _('Successfully Change Start Wash!'), 'wash_order_data':wash_order_data}
                elif search_wash_order and  context.get('emptying_wash_order'):
                    search_wash_order[0].write({'state':'start_emptying', 'start_datetime': p_time }) 

                    return {'success': _('Successfully Change Emplying!'), 'state': search_wash_order[0].state, #'wash_order_data':wash_order_data
				}
                elif search_wash_order and  context.get('compliance_wash_order'):
                    survey_container = self.env['ir.config_parameter'].sudo().get_param('container_compliance_id') 
                    survey_container_id =  survey_obj.search([('id', '=', survey_container)])
                    return {'success': _('Successfully Change Emplying!'), 'wash_order':search_wash_order[0],'survey_container_id':survey_container_id, }
                elif search_wash_order and  context.get('drying_wash_order'):
                    dangerous_characteristics = []
                    variants =[]
                    recycled_product_name = False
                    if search_wash_order[0].recycled_product_id:
                        recycled_product_name = search_wash_order[0].recycled_product_id.name
                    if search_wash_order[0].product_id.danger_char_ids:
                        for char in search_wash_order[0].product_id.danger_char_ids:
                           dangerous_characteristics.append(char.description)
                    if search_wash_order[0].product_id.attribute_value_ids:
                        for attr in search_wash_order[0].product_id.attribute_value_ids:
                           variants.append(attr.name)
                    wash_order_data = []
                    search_wash_order[0].write({'state':'start_drying', 'start_datetime': p_time })  
                    wash_order_data.append({
			'barcode': search_wash_order[0].lot_id.name,
                        'img_url': search_wash_order[0].product_id.image,
                         'order_number': search_wash_order[0].name,
			   'type_of_order':search_wash_order[0].type_of_order,
			   'dangerous_characteristics': dangerous_characteristics,
		           'state':search_wash_order[0].state,
			  'ler': search_wash_order[0].product_id.lercode_id.name or '',
			'un_code': search_wash_order[0].product_id.uncode or '',
			'variants':variants,
			'recycled_product' : recycled_product_name,
			'location_id':search_wash_order[0].location_id.name,
			'dest_location_id': search_wash_order[0].location_dest_id.name,
				})  
                    return {'success': _('Successfully Change Emplying!'),'wash_order_data':wash_order_data }
                elif search_crush_order and  context.get('start_crush_order'):
                    default_code = ''
                    search_recycled_product = False
                    dest_location = False
                    dest_name = False
                    if not context.get('recycled_product'):
                        return  {'warning1': _('Recycled Product missing!'), }
                    if not context.get('dest_location'):
                        return  {'warning2': _('Destination location is missing!'), }
                    if  context.get('recycled_product') and    context.get('dest_location'):
                        first_location_name =   context.get('dest_location').split('/')
                        if len(first_location_name) >= 3:
                            parent_location_search =  location_obj.search([('name','=' ,first_location_name[0])])
                            prent_of_parent_search = location_obj.search([('location_id','=' ,parent_location_search[0].id)])
                            location_search = location_obj.search([('name','=' ,first_location_name[2]), ('location_id','=', prent_of_parent_search[0].id)])
                        else:
                            parent_location_search =  location_obj.search([('name','=' ,first_location_name[0])])
                            location_search = location_obj.search([('name','=' ,first_location_name[-1]), ('location_id','=', parent_location_search[0].id)])
                        recycled_product = context.get('recycled_product').split(' ')
                        c =  recycled_product[0].replace('[','')
                        default_code = c.replace(']','')
                        search_recycled_product = product_obj.search([('default_code','=', default_code)])
                        if search_recycled_product:
                            search_recycled_product = search_recycled_product[0].id
                        if location_search:
                            dest_location = location_search[0].id
                            dest_name = location_search[0].name
                        search_crush_order[0].write({'state':'start_crush', 'start_datetime': p_time ,'recycled_product_id': search_recycled_product , 'location_dest_id': dest_location})    
                        dangerous_characteristics = []
                        variants =[]
                        recycled_product_name = False
                        if search_crush_order[0].recycled_product_id:
                            recycled_product_name = search_crush_order[0].recycled_product_id.name
                        if search_crush_order[0].product_id.danger_char_ids:
                            for char in search_crush_order[0].product_id.danger_char_ids:
                                dangerous_characteristics.append(char.description)
                        if search_crush_order[0].product_id.attribute_value_ids:
                            for attr in search_crush_order[0].product_id.attribute_value_ids:
                                variants.append(attr.name)
                        wash_order_data = []
                        wash_order_data.append({
			'barcode': search_crush_order[0].lot_id.name,
                        'img_url': search_crush_order[0].product_id.image,
                         'order_number': search_crush_order[0].name,
			   'type_of_order':search_crush_order[0].type_of_order,
			   'dangerous_characteristics': dangerous_characteristics,
		           'state':search_crush_order[0].state,
			  'ler': search_crush_order[0].product_id.lercode_id.name or '',
			'un_code': search_crush_order[0].product_id.uncode or '',
			'variants':variants,
			'kilo_qty':search_crush_order[0].product_id.plastic_kg or 0.0,
			'recycled_product' : recycled_product_name,
			'location_id':search_crush_order[0].location_id.name,
			'dest_location_id': dest_name,
				})  
                        return {'success': _('Successfully Change Emplying!'),'wash_order_data':wash_order_data }

                elif search_compact_order and  context.get('start_compact_order'):
                    default_code = ''
                    search_recycled_product = False
                    dest_location = False
                    dest_name = False
                    if not context.get('recycled_product'):
                        return  {'warning1': _('Recycled Product missing!'), }
                    if not context.get('dest_location'):
                        return  {'warning2': _('Destination location is missing!'), }
                    if  context.get('recycled_product') and    context.get('dest_location'): 
                        first_location_name =   context.get('dest_location').split('/')
                        if len(first_location_name) >= 3:
                            parent_location_search =  location_obj.search([('name','=' ,first_location_name[0])])
                            prent_of_parent_search = location_obj.search([('location_id','=' ,parent_location_search[0].id)])
                            location_search = location_obj.search([('name','=' ,first_location_name[2]), ('location_id','=', prent_of_parent_search[0].id)])
                        else:
                            parent_location_search =  location_obj.search([('name','=' ,first_location_name[0])])
                            location_search = location_obj.search([('name','=' ,first_location_name[-1]), ('location_id','=', parent_location_search[0].id)])
                        location =   context.get('dest_location').split('/')
                        recycled_product = context.get('recycled_product').split(' ')
                        c =  recycled_product[0].replace('[','')
                        default_code = c.replace(']','')
                        search_recycled_product = product_obj.search([('default_code','=', default_code)])
                        if search_recycled_product:
                            search_recycled_product = search_recycled_product[0].id
                        else:
                            search_recycled_product = product_obj.search([('name','=', default_code)])
                            search_recycled_product = search_recycled_product[0].id
                        if location_search:
                            dest_location = location_search[0].id
                            dest_name = location_search[0].name
                        search_compact_order[0].write({'state':'start_crush', 'start_datetime': p_time ,'recycled_product_id': search_recycled_product , 'location_dest_id': dest_location})  
                        dangerous_characteristics = []
                        variants =[]
                        recycled_product_name = False
                        if search_compact_order[0].recycled_product_id:
                            recycled_product_name = search_compact_order[0].recycled_product_id.name
                        if search_compact_order.product_id.danger_char_ids:
                            for char in search_compact_order.product_id.danger_char_ids:
                                dangerous_characteristics.append(char.description)

                        if search_compact_order.product_id.attribute_value_ids:
                            for attr in search_compact_order[0].product_id.attribute_value_ids:
                                variants.append(attr.name)
                        wash_order_data = []
                        wash_order_data.append({
			'barcode': search_compact_order.lot_id.name,
                        'img_url': search_compact_order.product_id.image,
                         'order_number': search_compact_order.name,
			   'type_of_order':search_compact_order.type_of_order,
			   'dangerous_characteristics': dangerous_characteristics,
		           'state':search_compact_order.state,
			  'ler': search_compact_order.product_id.lercode_id.name or '',
			'un_code': search_compact_order.product_id.uncode or '',
			'variants':variants,	
			'kilo_qty':search_compact_order[0].product_id.metal_kg or 0.0,
			'recycled_product' : recycled_product_name,
			'location_id':search_compact_order.location_id.name,
			'dest_location_id': dest_name,
				})  
                        return {'success': _('Successfully Change Emplying!'), 'wash_order_data':wash_order_data}

                elif search_wash_order and  context.get('pre_wash_order'):
                    search_wash_order[0].write({'state':'start_re_wash', 'start_datetime': p_time })  
                    return {'success': _('Successfully Change Pre-Wash!'),'state': search_wash_order[0].state , #'wash_order_data':wash_order_data
			 }
                elif search_wash_order and  context.get('start_wash_order'):
                    search_wash_order[0].write({'state':'start_wash', 'start_datetime': p_time })    
                    return {'success': _('Successfully Change Start Wash!'),'state':search_wash_order[0].state  }
                elif search_crush_order and  context.get('stop_crush_order'):
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(search_crush_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')
                    m , s = divmod(pausetime_diff.total_seconds(), 60)
                    h, m = divmod(m, 60)
                    dur_h = (_('%0*d') % (2, h))
                    dur_m = (_('%0*d') % (2, m * 1.677966102))
                    dur_s = (_('%0*d') % (2, s))
                    duration = dur_h + '.' + dur_m + '.' + dur_s
                    hr_duration = dur_h + '.' + dur_m 
                    amount = float(hr_duration)
                    timesheet_vals ={
			'name': 'Crushing Time',
                        'date': start_date,
			 'amount': amount,
			'account_id':account_id ,
                         'employee_id':emp_id ,
                         'time': duration}
                    search_crush_order[0].write({'state' : 'stop_crush','timesheet_ids': [(0,0, timesheet_vals)] })
                    dangerous_characteristics = []
                    variants =[]
                    recycled_product_name = False
                    if search_crush_order[0].recycled_product_id:
                        recycled_product_name = search_crush_order[0].recycled_product_id.name
                    if search_crush_order[0].product_id.danger_char_ids:
                        for char in search_crush_order[0].product_id.danger_char_ids:
                            dangerous_characteristics.append(char.description)
                    if search_crush_order[0].product_id.attribute_value_ids:
                        for attr in search_crush_order[0].product_id.attribute_value_ids:
                            variants.append(attr.name)
                    wash_order_data = []
                    wash_order_data.append({
			'barcode': search_crush_order[0].lot_id.name,
                        'img_url': search_crush_order[0].product_id.image,
                         'order_number': search_crush_order[0].name,
			   'type_of_order':search_crush_order[0].type_of_order,
			   'dangerous_characteristics': dangerous_characteristics,
		           'state':search_crush_order[0].state,
			  'ler': search_crush_order[0].product_id.lercode_id.name or '',
			'un_code': search_crush_order[0].product_id.uncode or '',
			'variants':variants,
			'recycled_product' : recycled_product_name,
			'location_id':search_crush_order[0].location_id.name,
			'dest_location_id': search_crush_order[0].location_dest_id.name,
				})  
                    return {'success': _('Successfully Change stop crush!'),'wash_order_data':wash_order_data }
                elif search_compact_order and  context.get('stop_compact_order'):
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(search_compact_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')
                    m , s = divmod(pausetime_diff.total_seconds(), 60)
                    h, m = divmod(m, 60)
                    dur_h = (_('%0*d') % (2, h))
                    dur_m = (_('%0*d') % (2, m * 1.677966102))
                    dur_s = (_('%0*d') % (2, s))
                    duration = dur_h + '.' + dur_m + '.' + dur_s
                    hr_duration = dur_h + '.' + dur_m 
                    amount = float(hr_duration)
                    timesheet_vals ={
			'name': 'Crushing Time',
                        'date': start_date,
			 'amount': amount,
			'account_id':account_id ,
                         'employee_id':emp_id ,
                         'time': duration}
                    search_compact_order[0].write({'state' : 'stop_crush','timesheet_ids': [(0,0, timesheet_vals)] })
                    dangerous_characteristics = []
                    variants =[]
                    recycled_product_name = False
                    if search_compact_order[0].recycled_product_id:
                        recycled_product_name = search_compact_order[0].recycled_product_id.name
                    if search_compact_order[0].product_id.danger_char_ids:
                        for char in search_compact_order[0].product_id.danger_char_ids:
                            dangerous_characteristics.append(char.description)
                    if search_compact_order[0].product_id.attribute_value_ids:
                        for attr in search_compact_order[0].product_id.attribute_value_ids:
                            variants.append(attr.name)
                    wash_order_data = []
                    wash_order_data.append({
			'barcode': search_compact_order[0].lot_id.name,
                        'img_url': search_compact_order[0].product_id.image,
                         'order_number': search_compact_order[0].name,
			   'type_of_order':search_compact_order[0].type_of_order,
			   'dangerous_characteristics': dangerous_characteristics,
		           'state':search_compact_order[0].state,
			  'ler': search_compact_order[0].product_id.lercode_id.name or '',
			'un_code': search_compact_order[0].product_id.uncode or '',
			'variants':variants,
			'recycled_product' : recycled_product_name,
			'location_id':search_compact_order[0].location_id.name,
			'dest_location_id': search_compact_order[0].location_dest_id.name,
				})  
                    return {'success': _('Successfully Change stop crush!'),'wash_order_data':wash_order_data }
                elif search_crush_order and  context.get('transferto_crush_order'):
                    if not search_crush_order.product_id.plastic_kg:
                        return {'warning': _('First Please Enter material Quantity in Recycled Product!'), }
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(search_crush_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')
                    m , s = divmod(pausetime_diff.total_seconds(), 60)
                    h, m = divmod(m, 60)
                    dur_h = (_('%0*d') % (2, h))
                    dur_m = (_('%0*d') % (2, m * 1.677966102))
                    dur_s = (_('%0*d') % (2, s))
                    duration = dur_h + '.' + dur_m + '.' + dur_s
                    hr_duration = dur_h + '.' + dur_m 
                    amount = float(hr_duration)
                    timesheet_vals ={
			'name': 'Crush to Transter store time',
                        'date': start_date,
			 'amount': amount,
			'account_id':account_id ,
                         'employee_id':emp_id ,
                        'time': duration,
				}
                    search_crush_order[0].write({'state' : 'transfer_to_store','crush_qty':search_crush_order.product_id.plastic_kg ,'timesheet_ids': [(0,0, timesheet_vals)] })
                    if search_crush_order[0].recycled_product_id:
                        '''lot_create_id = self.env['stock.production.lot'].create({
                           'product_id': search_crush_order[0].recycled_product_id.id,
                           'product_uom_id': search_crush_order[0].recycled_product_id.uom_id.id ,
                           'name': self.env['ir.sequence'].next_by_code('ballester.stock.production.lot')
				})'''
                        line_values = {  
                                    'product_id' : search_crush_order[0].recycled_product_id.id,
                                    'product_uom_id': search_crush_order[0].recycled_product_id.uom_id.id,
                                    'prod_lot_id' : search_crush_order[0].lot_id.id,
                                    'product_qty' : search_crush_order[0].product_id.plastic_kg,
                                    'location_id' : search_crush_order[0].location_id.id,
                                    'state': 'confirm',
                                    }
                        inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
                        inv_vals = {'name' :inventory_sequence,
                           'filter':'product',
                           'line_ids': [(0, 0,  line_values)],
                           'location_id' :search_crush_order[0].location_id.id,
                           'product_id': search_crush_order[0].recycled_product_id.id,
                           'wash_id': search_crush_order[0].id
                            }
                        pro_inv = inventory_obj.create(inv_vals)
                        pro_inv.action_start()
                        pro_inv.action_done()
                        return {'success': _('Successfully Change Transfer To store!'), }

                elif search_compact_order and  context.get('transferto_compact_order'):
                    if not search_compact_order.product_id.metal_kg:
                        return {'warning': _('First Please Enter material Quantity in Product!'), }
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(search_compact_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')
                    m , s = divmod(pausetime_diff.total_seconds(), 60)
                    h, m = divmod(m, 60)
                    dur_h = (_('%0*d') % (2, h))
                    dur_m = (_('%0*d') % (2, m * 1.677966102))
                    dur_s = (_('%0*d') % (2, s))
                    duration = dur_h + '.' + dur_m + '.' + dur_s
                    hr_duration = dur_h + '.' + dur_m 
                    amount = float(hr_duration)
                    timesheet_vals ={
			'name': 'Crush to Transter store time',
                        'date': start_date,
			 'amount': amount,
			'account_id':account_id ,
                         'employee_id':emp_id ,
                        'time': duration,
				}
                    search_compact_order[0].write({'state' : 'transfer_to_store','crush_qty':search_compact_order.product_id.metal_kg,'timesheet_ids': [(0,0, timesheet_vals)] })
                    if search_compact_order[0].recycled_product_id:
                        '''lot_create_id = self.env['stock.production.lot'].create({
                           'product_id': search_compact_order[0].recycled_product_id.id,
                           'product_uom_id': search_compact_order[0].recycled_product_id.uom_id.id ,
                           'name': self.env['ir.sequence'].next_by_code('ballester.stock.production.lot')
				})'''
                        line_values = {  
                                    'product_id' : search_compact_order[0].recycled_product_id.id,
                                    'product_uom_id': search_compact_order[0].recycled_product_id.uom_id.id,
                                    'prod_lot_id' : search_compact_order[0].lot_id.id,
                                    'product_qty' : search_compact_order[0].product_id.metal_kg,
                                    'location_id' : search_compact_order[0].location_id.id,
                                    'state': 'confirm',
                                    }
                        inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
                        inv_vals = {'name' :inventory_sequence,
                           'filter':'product',
                           'line_ids': [(0, 0,  line_values)],
                           'location_id' :search_compact_order[0].location_id.id,
                           'product_id': search_compact_order[0].recycled_product_id.id,
                           'wash_id': search_compact_order[0].id
                            }
                        pro_inv = inventory_obj.create(inv_vals)
                        pro_inv.action_start()
                        pro_inv.action_done()
                        return {'success': _('Successfully Change Transfer To store!'), }

                elif search_wash_order and  context.get('end_wash_order'):
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(search_wash_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')
                    m , s = divmod(pausetime_diff.total_seconds(), 60)
                    h, m = divmod(m, 60)
                    dur_h = (_('%0*d') % (2, h))
                    dur_m = (_('%0*d') % (2, m * 1.677966102))
                    dur_s = (_('%0*d') % (2, s))
                    duration = dur_h + '.' + dur_m + '.' + dur_s
                    hr_duration = dur_h + '.' + dur_m 
                    amount = float(hr_duration)
                    timesheet_vals ={
			'name': 'Washing Time',
                        'date': start_date,
			 'amount': amount,
			'account_id':account_id ,
                         'employee_id':emp_id ,
                         'time': duration}
                    search_wash_order[0].write({'state' : 'end_wash','timesheet_ids': [(0,0, timesheet_vals)] })
                    return {'success': _('Successfully Change Start Wash!'), }
                
                elif search_wash_order and  context.get('end_emptying_wash_order'):
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(search_wash_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')
                    m , s = divmod(pausetime_diff.total_seconds(), 60)
                    h, m = divmod(m, 60)
                    dur_h = (_('%0*d') % (2, h))
                    dur_m = (_('%0*d') % (2, m * 1.677966102))
                    dur_s = (_('%0*d') % (2, s))
                    duration = dur_h + '.' + dur_m + '.' + dur_s
                    hr_duration = dur_h + '.' + dur_m 
                    amount = float(hr_duration)
                    timesheet_vals ={
			'name': 'Emptying',
                        'date': start_date,
			 'amount': amount,
			'account_id':account_id ,
                         'employee_id':emp_id ,
                         'time': duration}
                    search_wash_order[0].write({'state' : 'stop_emptying','timesheet_ids': [(0,0, timesheet_vals)] })
                    return {'success': _('Successfully Change Start Wash!'), 
		#'wash_order_data':wash_order_data
			}
                elif search_wash_order and  context.get('end_prewash_order'):
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(search_wash_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')
                    m , s = divmod(pausetime_diff.total_seconds(), 60)
                    h, m = divmod(m, 60)
                    dur_h = (_('%0*d') % (2, h))
                    dur_m = (_('%0*d') % (2, m * 1.677966102))
                    dur_s = (_('%0*d') % (2, s))
                    duration = dur_h + '.' + dur_m + '.' + dur_s
                    hr_duration = dur_h + '.' + dur_m 
                    amount = float(hr_duration)
                    timesheet_vals ={
			'name': 'Pre-Washing Time',
                        'date': start_date,
			 'amount': amount,
			'account_id':account_id ,
                         'employee_id':emp_id ,
                         'time': duration}
                    search_wash_order[0].write({'state' : 'stop_re_wash','timesheet_ids': [(0,0, timesheet_vals)] })
                    dangerous_characteristics = []
                    variants =[]
                    recycled_product_name = False
                    if search_wash_order[0].recycled_product_id:
                        recycled_product_name = search_wash_order[0].recycled_product_id.name
                    if search_wash_order[0].product_id.danger_char_ids:
                        for char in search_wash_order[0].product_id.danger_char_ids:
                           dangerous_characteristics.append(char.description)
                    if search_wash_order[0].product_id.attribute_value_ids:
                        for attr in search_wash_order[0].product_id.attribute_value_ids:
                           variants.append(attr.name)
                    wash_order_data = []
                    wash_order_data.append({
			'barcode': search_wash_order[0].lot_id.name,
                        'img_url': search_wash_order[0].product_id.image,
                         'order_number': search_wash_order[0].name,
			   'type_of_order':search_wash_order[0].type_of_order,
			   'dangerous_characteristics': dangerous_characteristics,
		           'state':search_wash_order[0].state,
			  'ler': search_wash_order[0].product_id.lercode_id.name or '',
			'un_code': search_wash_order[0].product_id.uncode or '',
			'variants':variants,
			'recycled_product' : recycled_product_name,
			'location_id':search_wash_order[0].location_id.name,
			'dest_location_id': search_wash_order[0].location_dest_id.name,
				})  
                    return {'success': _('Successfully Change Start Wash!'), 'wash_order_data': wash_order_data }
               
                elif search_wash_order and  context.get('end_drying_wash_order'):
                    dangerous_characteristics = []
                    variants =[]
                    recycled_product_name = False
                    if search_wash_order[0].recycled_product_id:
                        recycled_product_name = search_wash_order[0].recycled_product_id.name
                    if search_wash_order[0].product_id.danger_char_ids:
                        for char in search_wash_order[0].product_id.danger_char_ids:
                           dangerous_characteristics.append(char.description)
                    if search_wash_order[0].product_id.attribute_value_ids:
                        for attr in search_wash_order[0].product_id.attribute_value_ids:
                           variants.append(attr.name)
                    wash_order_data = []
                    
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(search_wash_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')
                    m , s = divmod(pausetime_diff.total_seconds(), 60)
                    h, m = divmod(m, 60)
                    dur_h = (_('%0*d') % (2, h))
                    dur_m = (_('%0*d') % (2, m * 1.677966102))
                    dur_s = (_('%0*d') % (2, s))
                    duration = dur_h + '.' + dur_m + '.' + dur_s
                    hr_duration = dur_h + '.' + dur_m 
                    amount = float(hr_duration)
                    timesheet_vals ={
			'name': 'Drying Time',
                        'date': start_date,
			 'amount': amount,
			'account_id':account_id ,
                         'employee_id':emp_id ,
                         'time': duration}
                    search_wash_order[0].write({'state' : 'stop_drying','timesheet_ids': [(0,0, timesheet_vals)] })
                    wash_order_data.append({
			'barcode': search_wash_order[0].lot_id.name,
                        'img_url': search_wash_order[0].product_id.image,
                         'order_number': search_wash_order[0].name,
			   'type_of_order':search_wash_order[0].type_of_order,
			   'dangerous_characteristics': dangerous_characteristics,
		           'state':search_wash_order[0].state,
			  'ler': search_wash_order[0].product_id.lercode_id.name or  '',
			'un_code': search_wash_order[0].product_id.uncode or '',
			'variants':variants,
			'recycled_product' : recycled_product_name,
			'location_id':search_wash_order[0].location_id.name,
			'dest_location_id': search_wash_order[0].location_dest_id.name,
				})  
                    return {'success': _('Successfully Change End drying Wash!'),'wash_order_data': wash_order_data}
                elif search_wash_order and  context.get('backto_wash_order'):
                    if context.get('reason') == '\n' or context.get('reason') == '': 
                        return {'warning' : _('Please enter reason for back to Wash')}
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S')-datetime.strptime(str(search_wash_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')
                    m , s = divmod(pausetime_diff.total_seconds(), 60)
                    h, m = divmod(m, 60)
                    dur_h = (_('%0*d') % (2, h))
                    dur_m = (_('%0*d') % (2, m * 1.677966102))
                    dur_s = (_('%0*d') % (2, s))
                    duration = dur_h + '.' + dur_m+ '.' + dur_s
                    hr_duration = dur_h + '.' + dur_m 
                    amount = float(hr_duration)
                    timesheet_vals ={
                        'name': 'Back to Wash Time',
                          'date': start_date,
                         'amount': amount,
                        'account_id':account_id ,
                         'employee_id':emp_id ,
				}
                    search_wash_order[0].write({'state':'draft','internal_notes': context.get('reason'), 'timesheet_ids': [(0,0, timesheet_vals)]})  
                    return {'success': _('Successfully Change Start Wash!'), }

                elif search_wash_order and  context.get('destruction_wash_order'):
                    pro_line_values = {
                        'product_id': search_wash_order[0].product_id.id,
                        'product_uom_id': search_wash_order[0].product_id.uom_id.id,
                        'prod_lot_id': search_wash_order[0].lot_id.id,
                        'product_qty': 0,
                        'location_id': search_wash_order[0].location_id.id,
                        'state': 'confirm'
                    }
                    pro_inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
                    pro_inv_vals = {'name': pro_inventory_sequence,
                                    'filter': 'product',
                                    'line_ids': [(0, 0, pro_line_values)],
                                    'location_id': search_wash_order[0].location_id.id,
                                    'product_id': search_wash_order[0].product_id.id,
                                    'wash_id': search_wash_order[0].id
                                    }
                    pro_inv = inventory_obj.create(pro_inv_vals)
                    pro_inv.action_start()
                    pro_inv.action_done()
                    crush_container_vals = {
                        'name': self.env['ir.sequence'].next_by_code('wash.order.crush'),
                        'product_id': search_wash_order[0].product_id.id,
                        'type_of_order': 'crush',
                        'product_uom': search_wash_order[0].product_id.uom_id.id,
                        'lot_id': search_wash_order[0].lot_id.id,
                        'product_qty': 0,
                        'location_id': search_wash_order[0].location_id.id,
                        'location_dest_id': search_wash_order[0].location_dest_id.id,
                        'washing_type': search_wash_order[0].washing_type,
                        'wash_id': search_wash_order[0].id}

                    create_crush = self.env['wash.order'].create(crush_container_vals)
                    compact_container_vals = {
                        'name': self.env['ir.sequence'].next_by_code('wash.order.compact'),
                        'product_id': search_wash_order[0].product_id.id,
                        'type_of_order': 'compact',
                        'product_uom': search_wash_order[0].product_id.uom_id.id,
                        'lot_id': search_wash_order[0].lot_id.id,
                        'product_qty': 0,
                        'location_id': search_wash_order[0].location_id.id,
                        'location_dest_id': search_wash_order[0].location_dest_id.id,
                        'washing_type': search_wash_order[0].washing_type,
                        'wash_id': search_wash_order[0].id}
                    create_compact = self.env['wash.order'].create(compact_container_vals)
                    amount = 0.0

                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                        str(search_wash_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')

                    m, s = divmod(pausetime_diff.total_seconds(), 60)
                    h, m = divmod(m, 60)
                    dur_h = (_('%0*d') % (2, h))
                    dur_m = (_('%0*d') % (2, m * 1.677966102))
                    dur_s = (_('%0*d') % (2, s))
                    duration = dur_h + '.' + dur_m + '.' + dur_s
                    hr_duration = dur_h + '.' + dur_m
                    amount = float(hr_duration)
                    timesheet_vals = {
                        'name': 'Wash Container to Destruction Time',
                        'date': start_date,
                        'amount': amount,
                        'account_id': account_id,
                        'employee_id': emp_id,
                        'time': duration
                    }
                    search_wash_order[0].write({'state': 'destructed', 'timesheet_ids': [(0, 0, timesheet_vals)]})
                    return {'success': _('Successfully Change Start Wash!'), }

                elif search_drum_wash_order and  context.get('backto_drum_wash_order'):
                    
                    if context.get('reason') == '\n' or context.get('reason') == '': 
                        return {'warning' : _('Please enter reason for back to Wash')}
                    pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S')-datetime.strptime(str(search_drum_wash_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')
                    m , s = divmod(pausetime_diff.total_seconds(), 60)
                    h, m = divmod(m, 60)
                    dur_h = (_('%0*d') % (2, h))
                    dur_m = (_('%0*d') % (2, m * 1.677966102))
                    dur_s = (_('%0*d') % (2, s))
                    duration = dur_h + '.' + dur_m+ '.' + dur_s
                    hr_duration = dur_h + '.' + dur_m 
                    amount = float(hr_duration)
                    timesheet_vals ={
		        'name': 'Back to Wash Time',
		          'date': start_date,
		         'amount': amount,
		        'account_id':account_id ,
                          'employee_id':emp_id ,
				}
                    search_drum_wash_order[0].write({'state':'draft','internal_notes': context.get('reason'), 'timesheet_ids': [(0,0, timesheet_vals)]})  
                    return {'success': _('Successfully Change Start Wash!'), }

                elif search_drum_wash_order and  context.get('destruction_drum_wash_order'): 
                    if search_drum_wash_order[0].type_of_drum == 'plastic':
                        pro_line_values = {
                            'product_id': search_drum_wash_order[0].product_id.id,
                            'product_uom_id': search_drum_wash_order[0].product_id.uom_id.id,
                            'prod_lot_id': search_drum_wash_order[0].lot_id.id,
                            'product_qty': 0,
                            'location_id': search_drum_wash_order[0].location_id.id,
                            'state': 'confirm'
                        }
                        pro_inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
                        pro_inv_vals = {'name': pro_inventory_sequence,
                                        'filter': 'product',
                                        'line_ids': [(0, 0, pro_line_values)],
                                        'location_id': search_drum_wash_order[0].location_id.id,
                                        'product_id': search_drum_wash_order[0].product_id.id,
                                        'wash_id': search_drum_wash_order[0].id
                                        }
                        pro_inv = inventory_obj.create(pro_inv_vals)
                        pro_inv.action_start()
                        pro_inv.action_done()
                        amount = 0.0

                        pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                            str(search_drum_wash_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')

                        m, s = divmod(pausetime_diff.total_seconds(), 60)
                        h, m = divmod(m, 60)
                        dur_h = (_('%0*d') % (2, h))
                        dur_m = (_('%0*d') % (2, m * 1.677966102))
                        dur_s = (_('%0*d') % (2, s))
                        duration = dur_h + '.' + dur_m + '.' + dur_s
                        hr_duration = dur_h + '.' + dur_m
                        amount = float(hr_duration)
                        timesheet_vals = {
                            'name': 'Wash Drum to Destruction Time',
                            'date': start_date,
                            'amount': amount,
                            'account_id': account_id,
                            'employee_id': emp_id,
                            'time': duration
                        }
                        crush_drum_vals = {
                            'name': self.env['ir.sequence'].next_by_code('wash.order.crush'),
                            'product_id': search_drum_wash_order[0].product_id.id,
                            'type_of_order': 'crush',
                            'product_uom': search_drum_wash_order[0].product_id.uom_id.id,
                            'lot_id': search_drum_wash_order[0].lot_id.id,
                            'product_qty': 0,
			    'type_of_drum' :  search_drum_wash_order[0].type_of_drum,
                            'location_id': search_drum_wash_order[0].location_id.id,
                            'location_dest_id': search_drum_wash_order[0].location_dest_id.id,
                            'washing_type': search_drum_wash_order[0].washing_type,
                            'wash_id': search_drum_wash_order[0].id}

                        create_crush = self.env['wash.order'].create(crush_drum_vals)
                        search_drum_wash_order[0].write({'state': 'destructed', 'timesheet_ids': [(0, 0, timesheet_vals)]})
                        return {'success': _('Successfully Change Start Wash!'), }
                    elif search_drum_wash_order[0].type_of_drum ==  'metal':
                        pro_line_values = {
                            'product_id': search_drum_wash_order[0].product_id.id,
                            'product_uom_id': search_drum_wash_order[0].product_id.uom_id.id,
                            'prod_lot_id': search_drum_wash_order[0].lot_id.id,
                            'product_qty': 0,
                            'location_id': search_drum_wash_order[0].location_id.id,
                            'state': 'confirm'
                        }
                        pro_inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
                        pro_inv_vals = {'name': pro_inventory_sequence,
                                        'filter': 'product',
                                        'line_ids': [(0, 0, pro_line_values)],
                                        'location_id': search_drum_wash_order[0].location_id.id,
                                        'product_id': search_drum_wash_order[0].product_id.id,
                                        'wash_id': search_drum_wash_order[0].id
                                        }
                        pro_inv = inventory_obj.create(pro_inv_vals)
                        pro_inv.action_start()
                        pro_inv.action_done()
                        amount = 0.0

                        pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(
                            str(search_drum_wash_order[0].start_datetime), '%Y-%m-%d %H:%M:%S')

                        m, s = divmod(pausetime_diff.total_seconds(), 60)
                        h, m = divmod(m, 60)
                        dur_h = (_('%0*d') % (2, h))
                        dur_m = (_('%0*d') % (2, m * 1.677966102))
                        dur_s = (_('%0*d') % (2, s))
                        duration = dur_h + '.' + dur_m + '.' + dur_s
                        hr_duration = dur_h + '.' + dur_m
                        amount = float(hr_duration)
                        timesheet_vals = {
                            'name': 'Wash Drum to Destruction Time',
                            'date': start_date,
                            'amount': amount,
                            'account_id': account_id,
                            'employee_id': emp_id,
                            'time': duration
                        }
                        compact_drum_vals = {
                            'name': self.env['ir.sequence'].next_by_code('wash.order.compact'),
                            'product_id': search_drum_wash_order[0].product_id.id,
                            'type_of_order': 'compact',
                            'product_uom': search_drum_wash_order[0].product_id.uom_id.id,
                            'lot_id': search_drum_wash_order[0].lot_id.id,
                            'product_qty': 0,
			    'type_of_drum' :  search_drum_wash_order[0].type_of_drum,
                            'location_id': search_drum_wash_order[0].location_id.id,
                            'location_dest_id': search_drum_wash_order[0].location_dest_id.id,
                            'washing_type': search_drum_wash_order[0].washing_type, 'wash_id': search_drum_wash_order[0].id}
                        create_crush = self.env['wash.order'].create(compact_drum_vals)
                        search_drum_wash_order[0].write({'state': 'destructed', 'timesheet_ids': [(0, 0, timesheet_vals)]})
                        return {'success': _('Successfully Change Start Wash!'), }
                else:
                    print ("cccccccccaaaaaaaaaaa")
                    return {'warning':  'Please Enter Valid Number !'}                   
 
            else:
                print (">>>>>>>>>>>>>>>>>>Valid>>>>>>>>>>>>>")
                return {'warning':  'Please Enter Valid Number !'}

    # creating Wash Order
    @api.multi
    def create_wash_order_method(self, record_data):
        inventory_obj = self.env['stock.inventory']
        lot_obj = self.env['stock.production.lot']
        product_obj = self.env['product.product']
        inventory_adjustment_table = []
        ctx = dict(self._context)
        name = False
        type_of_order = False
        
        for data in record_data:
            for barcode in data.get('barcode_ids'):
                if data.get('type_of_order') == 'Container':
                    type_of_order = 'container'
                    name = self.env['ir.sequence'].next_by_code('wash.order.container') or _('New')
                if data.get('type_of_order') == 'Drum':
                    type_of_order = 'drum'
                    name = vals['name'] = self.env['ir.sequence'].next_by_code('wash.order.drum') or _('New')
                product_search_ids = product_obj.search([('id', '=', int(data.get('product_id')))])
                user_tz = self.env.user.tz
                local = pytz.timezone(user_tz)
                date = datetime.now(local)
                wash_data = {
                    'name': name,
                    'type_of_order': type_of_order,
                    'product_id': int(data.get('product_id')),
                    'recycled_product_id': int(data.get('recycled_product_id')),
                    'location_id': int(data.get('location')),
                    'location_dest_id': int(data.get('dest_location_id')),
                    'wash_date': date,
                    'product_qty': 1.0,
                    'product_uom': product_search_ids.uom_id.id,
                    'state': 'draft',
                    'lot_id': int(barcode),
                }
                create_wash_order = self.env['wash.order'].create(wash_data)
                if create_wash_order:
                    return {'success': "Successfully Created Wash Order!"}


    @api.multi
    def set_product_name(self, product):
        set_product = product.name
        if product.default_code and product.attribute_line_ids:
            variable_attributes = product.attribute_line_ids.filtered(lambda l: len(l.value_ids) > 1).mapped(
                'attribute_id')
            print (">>>>>>>>>>><MMMMM",variable_attributes)
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
    def save_repair_part(self, record_data,repair_order):
        barcode_list = []
        location_obj = self.env['stock.location']
        repair_search = self.env['mrp.repair'].search([('name','=', repair_order )])
        operation_val = []
        repair_data = []
        lot_search = False
        for rec in record_data:
            product_search = self.env['product.product'].search([('id','=', int(rec.get('product') )   )])
            args = repair_search.company_id and [('company_id', '=', repair_search.company_id.id)] or []
            warehouse = self.env['stock.warehouse'].search(args, limit=1)
            location_id = warehouse.lot_stock_id
            location_dest_id = location_obj.search([('usage', '=', 'production')], limit=1)
            if repair_search:
                vals = {
		    'type':'add',
                    'product_id': int(rec.get('product')),
                    'location_id': location_id.id,
                    'location_dest_id' :location_dest_id.id,
                    'price_unit': int(rec.get('qty')),
                    'name':  product_search[0].name,
		    'product_uom': product_search[0].uom_id.id
			}
                repair_data.append({
		    'product_id': product_search[0].display_name,
                    'location_id': location_id.display_name,
                    'location_dest_id' :location_dest_id[0].display_name,
                    'price_unit': int(rec.get('qty')),
                    'name':  product_search[0].name,

                               }
				)
                operation_val.append((0,0,vals))
        if repair_search:
            repair_search[0].operations = operation_val
            return {'success': 'Successfully Created' , 'repair_data': repair_data}
        else:
            return {'warning' : 'no repairorder'}

    @api.multi
    def edit_repair_part(self, record_data,repair_order):
        barcode_list = []
        repair_search = self.env['mrp.repair'].search([('name','=', repair_order )])
        operation_val = []
        repair_data = []
        for rec in record_data:
            product_search = self.env['product.product'].search([('id','=', int(rec.get('product') )   )])
            if rec.get('barcode') :
                lot_search = self.env['stock.production.lot'].search([('id','=', int(rec.get('barcode') )   )])
                if lot_search:
                    lot_name =lot_search[0].name
            location_search = self.env['stock.location'].search([('id','=', int(rec.get('location') )   )])
            location_dest_search = self.env['stock.location'].search([('id','=', int(rec.get('dest_location') )   )])
            if repair_search:
                vals = {
		    'type':'add',
                    'product_id': int(rec.get('product')),
                    'location_id': int(rec.get('location')),
                    'location_dest_id' :int(rec.get('dest_location')),
                    'lot_id' : int(rec.get('barcode')),
                    'price_unit': int(rec.get('qty')),
                    'name':  product_search[0].description,
		    'product_uom': product_search[0].uom_id.id
			}
                repair_data.append({
		    'product_id': product_search[0].display_name,
                    'location_id': location_search[0].display_name,
                    'location_dest_id' :location_dest_search[0].display_name,
                    'lot_id' : lot_search[0].name,
                    'price_unit': int(rec.get('qty')),
                    'name':  product_search[0].description,
                               }
				)
                operation_val.append((0,0,vals))
        if repair_search:
            repair_search[0].operations = operation_val
            return {'success': 'Successfully Created' , 'repair_data': repair_data}
        else:
            return {'warning' : 'no repairorder'}

    #  saving wash order
    @api.multi
    def save_wash_order_method(self, record_data):
        if record_data:
            for rec in record_data:
                if rec.get('barcode_ids'):
                    lot_ids = self.env['stock.production.lot'].search([('id', 'in', rec.get('barcode_ids'))])
                    if lot_ids:
                        if rec.get('product_id'):
                            for lot in lot_ids:
                                if lot.product_id.id != int(rec.get('product_id')):
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
