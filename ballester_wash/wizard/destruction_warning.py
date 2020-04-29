# -*- coding: utf-8 -*-
# Odoo, Open Source Ballester Screen.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#

from odoo import api, fields, models, _
import pytz 
from datetime import datetime

    
class DestructionWarning(models.TransientModel):
    _name = 'dustruction.warning'

    name  = fields.Char(string="Name")
    

    @api.multi
    def action_destruction(self):
        ctx= self._context
        inventory_obj = self.env['stock.inventory']
        wash_obj = self.env['wash.order'].browse(ctx.get('active_id'))
        user_tz = self.env.user.tz
        local = pytz.timezone(user_tz)
        #date = datetime.now(local)
        start_date = datetime.today()
        account_id = self.env.ref('ballester_wash.analytic_account_wash_id', False).id
        p_time = fields.Datetime.now(local)
        emp_id =False
        emp_id = self.env['hr.employee'].search([('user_id','=', self._uid)])
        if emp_id:
            emp_id = emp_id.id
        pro_line_values = {  
			    'product_id' :wash_obj.product_id.id,
			    'product_uom_id' :wash_obj.product_id.uom_id.id,
			    'prod_lot_id' :wash_obj.lot_id.id,
			    'product_qty' :0,
			    'location_id' :wash_obj.location_id.id,
			    'state':'confirm'
			    }
        pro_inventory_sequence = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
        pro_inv_vals = {'name' :pro_inventory_sequence,
		       'filter':'product',
		       'line_ids': [(0, 0,  pro_line_values)],
		       'location_id' :wash_obj.location_id.id,
		       'product_id': wash_obj.product_id.id,
		       'wash_id': wash_obj.id
			}
        pro_inv = inventory_obj.create(pro_inv_vals)
        pro_inv.action_start()
        pro_inv.action_done()  
        amount = 0.0
        if wash_obj and wash_obj.type_of_order == 'container':
            crush_container_vals = {  
				'name':  self.env['ir.sequence'].next_by_code('wash.order.crush'),
			    'product_id' :wash_obj.product_id.id,
			    'type_of_order': 'crush',			
			    'product_uom' :wash_obj.product_id.uom_id.id,
			    'lot_id' :wash_obj.lot_id.id,
			    'product_qty' :0,
			    'location_id' :wash_obj.location_id.id,
			    'location_dest_id' :wash_obj.location_dest_id.id,
			    'washing_type': wash_obj.washing_type,
			     'wash_id':wash_obj.id }

            create_crush = self.env['wash.order'].create(crush_container_vals)
            compact_container_vals = {  
				'name':  self.env['ir.sequence'].next_by_code('wash.order.compact'),
			    'product_id' :wash_obj.product_id.id,
			    'type_of_order': 'compact',			
			    'product_uom' :wash_obj.product_id.uom_id.id,
			    'lot_id' :wash_obj.lot_id.id,
			    'product_qty' :0,
			    'location_id' :wash_obj.location_id.id,
			    'location_dest_id' :wash_obj.location_dest_id.id,
			    'washing_type': wash_obj.washing_type,
			    'wash_id':wash_obj.id}
            create_compact = self.env['wash.order'].create(compact_container_vals)
            amount = 0.0
            
            pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(wash_obj.start_datetime), '%Y-%m-%d %H:%M:%S')
                
            m , s = divmod(pausetime_diff.total_seconds(), 60)
            h, m = divmod(m, 60)
            dur_h = (_('%0*d') % (2, h))
            dur_m = (_('%0*d') % (2, m * 1.677966102))
            dur_s = (_('%0*d') % (2, s))
            duration = dur_h + '.' + dur_m + '.' + dur_s
            hr_duration = dur_h + '.' + dur_m 
            amount = float(hr_duration)
            timesheet_vals ={
		'name': 'Wash Container to Destruction Time',
                'date': start_date,
		 'amount': amount,
		'account_id':account_id ,
                 'employee_id':emp_id ,
                 'time': duration
			}
            wash_obj.write({'state':'destructed','timesheet_ids': [(0,0, timesheet_vals)]})

        if wash_obj and wash_obj.type_of_order == 'drum' and wash_obj.type_of_drum == 'plastic':
            pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(wash_obj.start_datetime), '%Y-%m-%d %H:%M:%S')
                
            m , s = divmod(pausetime_diff.total_seconds(), 60)
            h, m = divmod(m, 60)
            dur_h = (_('%0*d') % (2, h))
            dur_m = (_('%0*d') % (2, m * 1.677966102))
            dur_s = (_('%0*d') % (2, s))
            duration = dur_h + '.' + dur_m + '.' + dur_s
            hr_duration = dur_h + '.' + dur_m 
            amount = float(hr_duration)
            timesheet_vals ={
		'name': 'Wash Drum to Destruction Time',
                'date': start_date,
		 'amount': amount,
		'account_id':account_id ,
                 'employee_id':emp_id ,
                 'time': duration
			}         
            crush_drum_vals = {  
				'name':  self.env['ir.sequence'].next_by_code('wash.order.crush'),
			    'product_id' :wash_obj.product_id.id,
			     'type_of_order': 'crush',			
			    'product_uom' :wash_obj.product_id.uom_id.id,
			    'lot_id' :wash_obj.lot_id.id,
			    'product_qty' :0,
			    'location_id' :wash_obj.location_id.id,
			    'location_dest_id' :wash_obj.location_dest_id.id,
			    'washing_type': wash_obj.washing_type,
					'wash_id':wash_obj.id}

            create_crush = self.env['wash.order'].create(crush_drum_vals)
            wash_obj.write({'state':'destructed','timesheet_ids': [(0,0, timesheet_vals)]})
        if wash_obj and wash_obj.type_of_order == 'drum' and wash_obj.type_of_drum == 'metal':
            amount = 0.0
            
            pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(wash_obj.start_datetime), '%Y-%m-%d %H:%M:%S')
                
            m , s = divmod(pausetime_diff.total_seconds(), 60)
            h, m = divmod(m, 60)
            dur_h = (_('%0*d') % (2, h))
            dur_m = (_('%0*d') % (2, m * 1.677966102))
            dur_s = (_('%0*d') % (2, s))
            duration = dur_h + '.' + dur_m + '.' + dur_s
            hr_duration = dur_h + '.' + dur_m 
            amount = float(hr_duration)
            timesheet_vals ={
		'name': 'Wash Drum to Destruction Time',
                'date': start_date,
		 'amount': amount,
		'account_id':account_id ,
                 'employee_id':emp_id ,
                 'time': duration
			}
            compact_drum_vals = {  
				'name':  self.env['ir.sequence'].next_by_code('wash.order.compact'),
			    'product_id' :wash_obj.product_id.id,
			     'type_of_order': 'compact',			
			    'product_uom' :wash_obj.product_id.uom_id.id,
			    'lot_id' :wash_obj.lot_id.id,
			    'product_qty' :0,
			    'location_id' :wash_obj.location_id.id,
			    'location_dest_id' :wash_obj.location_dest_id.id,
			    'washing_type': wash_obj.washing_type,'wash_id':wash_obj.id}
            create_crush = self.env['wash.order'].create(compact_drum_vals)
            wash_obj.write({'state':'destructed','timesheet_ids': [(0,0, timesheet_vals)]})
        return True
     

