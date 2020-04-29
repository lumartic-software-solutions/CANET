# -*- coding: utf-8 -*-
# Odoo, Open Source Member Barcode Scanner.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#
from odoo import  http, _
from odoo.http import request


class EventBarcode(http.Controller):

    # scan barcode
    @http.route('/member_barcode_scanner/register_attendee', type='json', auth="user")
    def register_attendee(self, barcode, **kw):
        
        context = dict(request.context)
        print (">>>>>>>>>>>>>>>>>>>>>>",context ,self , )
        employee = request.env['hr.employee'].search([('barcode', '=', barcode)], limit=1)
        if employee :
            if not employee.user_id:
                return {'warning': _('Please Set Related User For Employee "%s" !') % employee.name}
            else:
                return {'success' :'Valid Barcode!', 'attendance_state':employee.attendance_state, 'employee_id':employee.id, 'employee': employee.name, 'employee_image_url' : employee.image}
        else:
            return {'warning': 'Invalid Barcode!'}
