#  -*- coding: utf-8 -*-
#  Odoo, Open Source Ballester Screen.
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl
{
    'name': 'Ballester Screen',
    'category': 'Inventory',
    'author': 'ITMusketeers Consultancy Services LLP',
    'description': """
================================================================================

1.  To View Ballester Screen.

================================================================================
""",
    'depends': ['member_barcode_scanner', 'product_expiry', 'itm_material', 'ballester_wash','product', 'base', 'web', 'stock', 'sale_management', 'ballester_product', 'hr'],
    'summary': 'To View Ballester Screen.',

    'data': [ 
		'security/screen_security.xml',
	         'data/adjustments_sequence_data.xml',
             'data/product_demo.xml',
             'views/asset.xml',
             'views/ballester_screen_view.xml',
             'views/stock_inventory_view.xml',
             'wizard/lot_details_wizard.xml',
             'report/template_barcode_report.xml',
             'custom_report.xml',
            ],
    'qweb': [
        "static/src/xml/current_login_user.xml",
        "static/src/xml/exit_popup_view.xml",
      "static/src/xml/task_confirm_template.xml",
        "static/src/xml/inventory_adjustments_view.xml",
        "static/src/xml/internal_transfer_view.xml",
        "static/src/xml/main_screen_template.xml",
        "static/src/xml/output_of_products_view.xml",
        "static/src/xml/warehouse_view.xml",
        "static/src/xml/generate_barcode_view.xml",
        "static/src/xml/barcode_receipt_template.xml",
        'static/src/xml/confirm_template.xml'
    ],
    'installable': True,

}
