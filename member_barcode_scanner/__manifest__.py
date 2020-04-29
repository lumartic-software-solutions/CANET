# -*- coding: utf-8 -*-
# Odoo, Open Source Member Barcode Scanner.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#
{
    'name'          : "Member Barcode Scanner",
    'summary'       : """Member Barcode Scanner""",
    'description'   : """
                    Barcode Scanner
    """,
    'author'        : "Pseudocode",
    'website'       : "www.pseudocode.co",
    'category'      : 'Hidden',
    'version'       : '1.0',
    'depends'       : ['hr_attendance', 'muk_web_client_notification', 'itm_material'],
    'data'          : [
        'views/res_company_view.xml',
        'views/member_barcode_view.xml',
        'views/template.xml',
        'views/user_view.xml',
    ],
    'qweb': [
        "static/src/xml/attendance.xml",
    ],
}
