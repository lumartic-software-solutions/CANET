#  -*- coding: utf-8 -*-
#  Odoo, Open Source Ballester Product.
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl
{
    'name': 'Ballester Product',
    'category': 'Product',
    'author': 'ITMusketeers Consultancy Services LLP',
    'description': """
================================================================================

1.  Ballester Product.
2.  Web CRM.

================================================================================
""",
    'depends': [ 'base', 'web','sale_management','delivery','stock','sale','purchase'],
    'summary': 'Customization in Product.',

    'data': [
            # 'wizard/sale_dms_wizard_view.xml',
            #'views/sale_dms_survey_view.xml',
            'security/ir.model.access.csv',
            'data/serial_sequence_data.xml',
            'views/asset.xml',
            'views/product_view.xml',
            'views/stock_production_lot_view.xml',
            'views/lot_attribute_view.xml',
            ],
    'installable': True,

}
