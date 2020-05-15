# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#
{
    "name": "Canet Screen",
    "summary": "Canet Screen",
    "version": "11.0",
    "category": "Operation",
    "author": 'Divya Vyas',

    "description": """
================================================================================

1.Create screen for warehouse

================================================================================
""",
    'depends': ['base', 'sale','stock','hr','member_barcode_scanner'],
    'data': [
            'data/adjustments_sequence_data.xml',
            'data/product_demo.xml',
            'report/template_barcode_report.xml',
            'views/custom_report.xml',
            'views/assets.xml',
            'views/stock_inventory_view.xml',
            'views/canet_screen_view.xml',

    ],
    'qweb': [
        "static/src/xml/main_screen_template.xml",
        "static/src/xml/warehouse_view.xml",
        "static/src/xml/exit_popup_view.xml",
        "static/src/xml/current_login_user.xml",
        "static/src/xml/generate_barcode_view.xml",
        "static/src/xml/inventory_adjustments_view.xml",
        "static/src/xml/internal_transfer_view.xml",
        "static/src/xml/internal_destruction_template.xml",
        "static/src/xml/barcode_receipt_template.xml"
        ],
    'application': True,
    'auto_install': False,
    'installable': True,

}