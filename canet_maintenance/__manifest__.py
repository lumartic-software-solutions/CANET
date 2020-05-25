# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#
{
    "name": "Canet Maintenance",
    "summary": "Customization in maintenance",
    "version": "11.0",
    "category": "Maintenance",
    "author": 'Divya Vyas',

    "description": """
================================================================================

1.Customization in Maintenanace

================================================================================
""",
    'depends': ['base', 'maintenance', 'account', 'stock', 'hr_timesheet'],
    'data': [
        'data/ir_sequence_data.xml',
        'data/analytic_account.xml',
        'security/ir.model.access.csv',
        'wizard/task_time_wizard_view.xml',
        'views/assets.xml',
        'views/maintenance_views.xml',
        'views/maintenance_timesheet_menu.xml',
    ],
    'qweb': [],
    'application': True,
    'auto_install': False,
    'installable': True,

}
