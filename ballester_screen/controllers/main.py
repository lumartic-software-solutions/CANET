# # -*- coding: utf-8 -*-
# # Odoo, Open Source Ballester Screen.
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#
# 
# import base64
# 
# from odoo import http, _
# from odoo.http import request
# from odoo.addons.base.ir.ir_qweb import AssetsBundle
# from odoo.addons.web.controllers.main import binary_content
# 
# 
# class BallesterScreen(http.Controller):
#     
#     
#     @http.route('/', type='json', auth="public") 
#     def get_root_submit(self, **post):
#         if post:
#             get_msg = post['send_msg']
#             getmessageobj = request.env['get.message']
#             rootmessageobj = request.env['root.message']
#             root_user_id = request.env['res.users'].search([('name', '=', 'root')], limit=1)
#             pass_value = {'root_name':'Root', 'send_msg':'Error'}
#             if root_user_id:
#                 if 'how are you?' == get_msg:
#                     send_msg = ' I am Fine. Thank You !'
#                     values = {
#                     'get_messages': send_msg ,
#                     'user_id': root_user_id.id}
#                     getmessageobj.create(values)
#     #                 rootmessageobj.create(values)
#                     pass_value = {'root_name' :'Root', 'send_msg' :send_msg} 
#                 elif 'you know who am i ?' == get_msg:
#                     current_user_id = request.env['res.users'].browse(request._uid)
#                     send_msg = 'Yes Your are ' + current_user_id.name + '.'
#                     values = {
#                     'get_messages': send_msg ,
#                     'user_id': root_user_id.id}
#                     getmessageobj.create(values)
#     #                 rootmessageobj.create(values)
#                     pass_value = {'root_name' :'Root', 'send_msg' :send_msg}
#                 elif 'good night' == get_msg:
#                     send_msg = 'Good Night.Sweet Dream'
#                     values = {
#                     'get_messages': send_msg ,
#                     'user_id': root_user_id.id}
#                     getmessageobj.create(values)
#     #                 rootmessageobj.create(values)
#                     pass_value = {'root_name' :'Root', 'send_msg' :send_msg}   
#                 elif 'bye' == get_msg:
#                     send_msg = 'Bye & Take Care.'
#                     values = {
#                     'get_messages': send_msg ,
#                     'user_id': root_user_id.id}
#                     getmessageobj.create(values)
#     #                 rootmessageobj.create(values)
#                     pass_value = {'root_name' :'Root', 'send_msg' :send_msg}   
#             return pass_value
#         else :
#             pass_value = {'root_name':'Root', 'send_msg':'Error'}
#             return pass_value
    


