from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError

import time
import pytz


# create new wizard object for manage task(start,end,stop)  
class TimePartWizard(models.TransientModel):
    _name = 'time.part.wizard'
    
    name = fields.Char(string="Name")
    description = fields.Text("Description")
    
    @api.model
    def default_get(self, vals):
        result = super(TimePartWizard, self).default_get(vals)
        context = self.env.context
        wash_obj = self.env['wash.order'].search([('id','=', context.get('active_id'))])
        if context.get('start_emptying'):
            result.update({'name' : "Are you sure You want to start emptying?"})
        if context.get('stop_emptying'):
            result.update({'name' : "Are you sure You want to End emptying?"})
        if context.get('start_re_wash'):
            result.update({'name' : "Are you sure You want to start Pre-Wash?"})
        if context.get('stop_re_wash'):
            result.update({'name' : "Are you sure You want to End Pre-Wash?"})
        if context.get('start_wash'):
            result.update({'name' : "¿Estás seguro de que quieres empezar a lavar?"})
        if context.get('end_wash'):
            result.update({'name' : "¿Vas a terminar el lavado?" })
        if context.get('start_drying'):
            result.update({'name' : "¿Seguro que quieres empezar a secar?" })
        if context.get('end_drying'):
            result.update({'name' : "¿Seguro que quieres dejar de secar?"})
        if context.get('start_repair'):
            result.update({'name' : "Are you sure You want to start repair?"})
        if context.get('end_repair'):
            result.update({'name' : "Are you sure You want to End repair?"})
        if context.get('crush_start'):
            result.update({'name' : "Are you sure You want to Start Crush/Compact Process?"})
        if context.get('crush_end'):
            result.update({'name' : "Are you sure You want to End Crush/Compact Process?"})
        if context.get('wash_cancel'):
            result.update({'name' : "Are you sure You want to Cancel Process?"})
        if context.get('crush_transfer_to_store'):
            result.update({'name' : "¿Estás seguro de que quieres transferir el producto a la tienda?"})
        if context.get('transfer_store'):
            if wash_obj:
                if wash_obj.repair_compliance =='no':
                    result.update({'name' : "You are trying to  transfer the product which related Repair has negative Compliance, Please Contact your Officer"})
                else:
                    result.update({'name' : "¿Estás seguro de que quieres transferir el producto a la tienda?"})
        return result
    
# button method of manage task and calculate duration
    @api.multi
    def accept_task(self):
        context = self._context
        wash_ids = self.env['wash.order'].sudo().search([('id', '=', context.get('active_id'))])
        repair_ids = self.env['mrp.repair'].sudo().search([('id', '=', context.get('active_id'))])
        data_list = []
        user_tz = self.env.user.tz
        local = pytz.timezone(user_tz)
        start_date = datetime.today()
        p_time = fields.Datetime.now(local)
        inventory_obj = self.env['stock.inventory']
        amount = 0.0
        emp_id =False
        emp_id = self.env['hr.employee'].search([('user_id','=', self._uid)])
        if emp_id:
            emp_id = emp_id.id
        account_id = self.env.ref('ballester_wash.analytic_account_wash_id', False).id
        if context.get('ok') and context.get('start_emptying') and context.get('active_model') == 'wash.order':
            if wash_ids:
                wash_ids.write({'state' : 'start_emptying', 'start_datetime' : p_time})
        if context.get('ok') and context.get('start_re_wash') and context.get('active_model') == 'wash.order':
            if wash_ids:
                wash_ids.write({'state' : 'start_re_wash', 'start_datetime' : p_time})
        if context.get('ok') and context.get('start_wash') and context.get('active_model') == 'wash.order':
            if wash_ids:
                wash_ids.write({'state' : 'start_wash', 'start_datetime' : p_time})
        if context.get('ok') and context.get('start_repair') and context.get('active_model') == 'mrp.repair':
            if repair_ids:
                repair_ids.write({'state' : 'under_repair', 'start_datetime' : p_time})
        if context.get('ok') and context.get('start_drying') and context.get('active_model') == 'wash.order':
            if wash_ids:
                wash_ids.write({'state' : 'start_drying', 'start_datetime' : p_time})
        if context.get('ok') and context.get('crush_start') and context.get('active_model') == 'wash.order':
            if wash_ids:
                wash_ids.write({'state' : 'start_crush', 'start_datetime' : p_time})
        if context.get('ok') and context.get('start_drying') and context.get('active_model') == 'wash.order':
            if wash_ids:
                wash_ids.write({'state' : 'start_drying', 'start_datetime' : p_time})
        if context.get('ok') and context.get('end_repair') and context.get('active_model') == 'mrp.repair':
            if repair_ids:
                pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(repair_ids.start_datetime), '%Y-%m-%d %H:%M:%S')
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
                    'time': duration
                }
                repair_ids.write({'state' : 'done','timesheet_ids': [(0,0, timesheet_vals)] })

        if context.get('ok') and context.get('end_wash') and context.get('active_model') == 'wash.order':
            if wash_ids:
                pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(wash_ids.start_datetime), '%Y-%m-%d %H:%M:%S')
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
                         'time': duration
				}
                wash_ids.write({'state' : 'end_wash','timesheet_ids': [(0,0, timesheet_vals)] })
        ######################emptying##############3
        if context.get('ok') and context.get('stop_emptying') and context.get('active_model') == 'wash.order':
            if wash_ids:
                pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(wash_ids.start_datetime), '%Y-%m-%d %H:%M:%S')
                m , s = divmod(pausetime_diff.total_seconds(), 60)
                h, m = divmod(m, 60)
                dur_h = (_('%0*d') % (2, h))
                dur_m = (_('%0*d') % (2, m * 1.677966102))
                dur_s = (_('%0*d') % (2, s))
                duration = dur_h + '.' + dur_m + '.' + dur_s
                hr_duration = dur_h + '.' + dur_m 
                amount = float(hr_duration)
                timesheet_vals ={

			'name': 'Empltying Time',
                        'date': start_date,
			'amount': amount,
			'account_id':account_id ,
                        'employee_id':emp_id ,
                        'time': duration,
          
				}
                wash_ids.write({'state' : 'stop_emptying','timesheet_ids': [(0,0, timesheet_vals)] })


        if context.get('ok') and context.get('wash_cancel') and context.get('active_model') == 'wash.order':
            if wash_ids:
                pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(wash_ids.start_datetime), '%Y-%m-%d %H:%M:%S')
                m , s = divmod(pausetime_diff.total_seconds(), 60)
                h, m = divmod(m, 60)
                dur_h = (_('%0*d') % (2, h))
                dur_m = (_('%0*d') % (2, m * 1.677966102))
                dur_s = (_('%0*d') % (2, s))
                duration = dur_h + '.' + dur_m + '.' + dur_s
                hr_duration = dur_h + '.' + dur_m 
                amount = float(hr_duration)
                timesheet_vals ={

			'name': 'start to cancel Time',
                        'date': start_date,
			'amount': amount,
			'account_id':account_id ,
                        'employee_id':emp_id ,
                        'time': duration,
          
				}
                wash_ids.write({'state' : 'cancel','timesheet_ids': [(0,0, timesheet_vals)] })

        if context.get('ok') and context.get('stop_re_wash') and context.get('active_model') == 'wash.order':
            if wash_ids:
                pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(wash_ids.start_datetime), '%Y-%m-%d %H:%M:%S')
                m , s = divmod(pausetime_diff.total_seconds(), 60)
                h, m = divmod(m, 60)
                dur_h = (_('%0*d') % (2, h))
                dur_m = (_('%0*d') % (2, m * 1.677966102))
                dur_s = (_('%0*d') % (2, s))
                duration = dur_h + '.' + dur_m + '.' + dur_s
                hr_duration = dur_h + '.' + dur_m 
                amount = float(hr_duration)
                timesheet_vals ={

			'name': 'Pre-Wash Time',
                        'date': start_date,
			'amount': amount,
			'account_id':account_id ,
                        'employee_id':emp_id ,
                        'time': duration,
          
				}
                wash_ids.write({'state' : 'stop_re_wash','timesheet_ids': [(0,0, timesheet_vals)] })



        if context.get('ok') and context.get('crush_end') and context.get('active_model') == 'wash.order':
            if wash_ids:
                pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(wash_ids.start_datetime), '%Y-%m-%d %H:%M:%S')
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
                         'time': duration
				}
                wash_ids.write({'state' : 'stop_crush','timesheet_ids': [(0,0, timesheet_vals)] })

        if context.get('ok') and context.get('end_drying') and context.get('active_model') == 'wash.order':
            if wash_ids:
                pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(wash_ids.start_datetime), '%Y-%m-%d %H:%M:%S')
                
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
                         'time': duration
				}
                wash_ids.write({'state' : 'stop_drying','timesheet_ids': [(0,0, timesheet_vals)] ,'start_datetime' : p_time})
        if context.get('ok') and context.get('crush_transfer_to_store') and context.get('active_model') == 'wash.order':
            if wash_ids:
                if not wash_ids.crush_qty:
                    raise UserError(_("Please Enter Quantity of Crush/Compact Material"))
                pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(wash_ids.start_datetime), '%Y-%m-%d %H:%M:%S')
                
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
                wash_ids.write({'state' : 'transfer_to_store','timesheet_ids': [(0,0, timesheet_vals)] })
                
                if wash_ids[0].recycled_product_id:
                    ###recycled product inventory
                    #lot_create_id = self.env['stock.production.lot'].create({'product_id': wash_ids[0].recycled_product_id.id,'product_uom_id': wash_ids[0].recycled_product_id.uom_id.id ,'name':self.env['ir.sequence'].next_by_code('ballester.stock.production.lot')})
                    line_values = {  
                                    'product_id' :wash_ids[0].recycled_product_id.id,
                                    'product_uom_id' :wash_ids[0].recycled_product_id.uom_id.id,
                                    'prod_lot_id' : wash_ids[0].lot_id.id,
                                    'product_qty' : wash_ids[0].crush_qty,
                                    'location_id' :wash_ids[0].location_id.id,
                                    'state':'confirm'
                                    }
                    inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
                    inv_vals = {'name' :inventory_sequence,
                           'filter':'product',
                           'line_ids': [(0, 0,  line_values)],
                           'location_id' :wash_ids[0].location_id.id,
                           'product_id': wash_ids[0].recycled_product_id.id,
                           'wash_id': wash_ids[0].id
                            }
                    pro_inv = inventory_obj.create(inv_vals)
                    pro_inv.action_start()
                    pro_inv.action_done()
                    
        if context.get('ok') and context.get('transfer_store') and context.get('active_model') == 'wash.order':
            if wash_ids:
                pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(wash_ids.start_datetime), '%Y-%m-%d %H:%M:%S')
                
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
                wash_ids.write({'state' : 'transfer_to_store','timesheet_ids': [(0,0, timesheet_vals)] ,'end_wash_datetime' : p_time})
                
                if wash_ids[0].recycled_product_id:
                    pro_line_values = {  
                                    'product_id' :wash_ids[0].product_id.id,
                                    'product_uom_id' :wash_ids[0].product_id.uom_id.id,
                                    'prod_lot_id' :wash_ids[0].lot_id.id,
                                    'product_qty' :0,
                                    'location_id' :wash_ids[0].location_id.id,
                                    'state':'confirm'
                                    }
                    pro_inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
                    pro_inv_vals = {'name' :pro_inventory_sequence,
                           'filter':'product',
                           'line_ids': [(0, 0,  pro_line_values)],
                           'location_id' :wash_ids[0].location_id.id,
                           'product_id': wash_ids[0].product_id.id,
                           'wash_id': wash_ids[0].id
                            }
                    pro_inv = inventory_obj.create(pro_inv_vals)
                    pro_inv.action_start()
                    pro_inv.action_done()
                    ###recycled product inventory
                    #lot_create_id = self.env['stock.production.lot'].create({'product_id': wash_ids[0].recycled_product_id.id,'product_uom_id': wash_ids[0].recycled_product_id.uom_id.id ,'name':self.env['ir.sequence'].next_by_code('ballester.stock.production.lot')})
                    line_values = {  
                                    'product_id' :wash_ids[0].recycled_product_id.id,
                                    'product_uom_id' :wash_ids[0].recycled_product_id.uom_id.id,
                                    'prod_lot_id' :wash_ids[0].lot_id.id,
                                    'product_qty' : 1,
                                    'location_id' :wash_ids[0].location_id.id,
                                    'state':'confirm'
                                    }
                    inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
                    inv_vals = {'name' :inventory_sequence,
                           'filter':'product',
                           'line_ids': [(0, 0,  line_values)],
                           'location_id' :wash_ids[0].location_id.id,
                           'product_id': wash_ids[0].recycled_product_id.id,
                           'wash_id': wash_ids[0].id
                            }
                    pro_inv = inventory_obj.create(inv_vals)
                    pro_inv.action_start()
                    pro_inv.action_done()
        return True


