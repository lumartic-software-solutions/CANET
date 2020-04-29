# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
import pytz

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class GobackWash(models.TransientModel):

    _name = "go.back.wash"

    note = fields.Text('Reason',required=True)

    @api.multi
    def go_back_button(self):
        ctx= self._context
        wash_obj = self.env['wash.order'] 
        user_tz = self.env.user.tz
        local = pytz.timezone(user_tz)
        if ctx.get('ok'):
            if ctx.get('active_id'):
                emp_id = False
                start_date = datetime.today(local)
                brw_wash =  wash_obj.browse(ctx.get('active_id'))
                p_time = fields.Datetime.now(local)
                emp_id = self.env['hr.employee'].search([('user_id','=', self._uid)])
                if emp_id:
                    emp_id = emp_id.id
                pausetime_diff = datetime.strptime(str(p_time), '%Y-%m-%d %H:%M:%S') - datetime.strptime(str(brw_wash.start_datetime), '%Y-%m-%d %H:%M:%S')
                account_id = self.env.ref('ballester_wash.analytic_account_wash_id', False).id
                m , s = divmod(pausetime_diff.total_seconds(), 60)
                h, m = divmod(m, 60)
                dur_h = (_('%0*d') % (2, h))
                dur_m = (_('%0*d') % (2, m * 1.677966102))
                dur_s =  (_('%0*d') % (2, s))
                duration = dur_h + '.' + dur_m + '.' + dur_s
                hr_duration = dur_h + '.' + dur_m 
                amount = float(hr_duration)
                timesheet_vals ={
			'name': 'Back to Wash Time',
                        'date': start_date,
			 'amount': amount,
			'account_id':account_id ,
                         'employee_id':emp_id ,
				}
                brw_wash.write({'state':'draft','internal_notes': self.note ,'timesheet_ids': [(0,0, timesheet_vals)]})
        return True     
