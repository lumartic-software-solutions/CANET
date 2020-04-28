# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#
{
    "name": "Canet Project",
    "summary": "Customization in Project",
    "version": "11.0",
    "category": "Project",
    "author": 'Divya Vyas',

    "description": """
================================================================================

1.Customization in Project Task

================================================================================
""",
    'depends': ['base','account','project','hr_timesheet','canet_maintenance'],
    'data': [
        'wizard/task_time_wizard_view.xml',
        'views/project_task_view.xml'

    ],
    'qweb': [],
    'application': True,
    'auto_install': False,
    'installable': True,

}