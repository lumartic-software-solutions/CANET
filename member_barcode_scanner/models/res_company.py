# -*- coding: utf-8 -*-
# Odoo, Open Source Member Barcode Scanner.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#

from odoo import  fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    access_kiosk_mode_notification = fields.Boolean(string="Kiosk Mode Notification")


class ResCompany(models.Model):
    _inherit = 'res.company'

    receipt_to_printer = fields.Boolean(
        string="Send Receipt to printer?",
    )
    ip_address = fields.Char(
        string="IP Address",
    )
    port = fields.Char(
        string="Port",
    )
    
