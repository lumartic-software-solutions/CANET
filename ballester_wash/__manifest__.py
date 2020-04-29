# -*- coding: utf-8 -*-
# Odoo, Open Source Ballester Washed Screen.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#
{
    'name': 'Ballester Washed Screen',
    'category': 'Manufacturing',
    'author': 'Divya Vyas',
    'description': """
================================================================================

1.  To View Ballester Washed Screen.

================================================================================
""",
    'depends': [  'base', 'web','member_barcode_scanner','stock','mrp_repair','ballester_product','product','hr_timesheet','survey'],
    'summary': 'To View Ballester Washed Screen.',

    'data': [ 
		'security/ir.model.access.csv',
		'security/wash_security.xml',
		'wizard/transfer_location_view.xml',
		'data/ir_sequence_data.xml',
		#'data/product_data.xml',
                'data/product_search_parameter.xml',
		'data/analytic_account.xml',
		'wizard/goback_view.xml',
                'wizard/destruction_warning_view.xml',
		'wizard/time_part_wizard_view.xml',
		
		'wizard/repair_wizard_view.xml',
		'views/asset.xml',
                'views/wash_screen_menu.xml',
		
		'views/hr_timesheet_view.xml',
		'views/wash_timesheet_menu.xml',
                'views/wash_order_view.xml',
		'views/product_view.xml',
		'views/mrp_repair_view.xml',
		'report/wash_order_reports.xml',
		'report/templates_wash_order.xml',
            ],
   'qweb': [
	
	"static/src/xml/confirm_task_template.xml",
        "static/src/xml/main_screen_wash_container.xml",
	   "static/src/xml/current_login_user.xml",
	
	   "static/src/xml/exit_popup_view.xml",
	"static/src/xml/container_display_screen_template.xml",
	"static/src/xml/confirm_template.xml",
	"static/src/xml/screen_container_drying_control.xml",
	"static/src/xml/screen_crush_compact.xml",
	"static/src/xml/container_drying_wash_display_screen_template.xml",
	"static/src/xml/drum_drying_wash_display_screen_template.xml",
	"static/src/xml/crush_compact_display_screen_template.xml",
	"static/src/xml/compact_display_screen.xml",
        "static/src/xml/crush_display_screen.xml",
	"static/src/xml/confirm_compliance_template.xml",
	"static/src/xml/confirm_repair_template.xml",

	
	"static/src/xml/crush_compact_create_menu_screen.xml",
	"static/src/xml/crush_compact_create_display_screen.xml",
	"static/src/xml/addpart_screen.xml",
	"static/src/xml/repair_order_dispay_template.xml",
	"static/src/xml/compliance_diplay_screen.xml",
	"static/src/xml/container_end_wash_display_screen_template.xml",
	"static/src/xml/screen_drum_drying_control.xml",
	"static/src/xml/screen_end_container.xml",
    ],


#     ],
    'installable': True,

}
