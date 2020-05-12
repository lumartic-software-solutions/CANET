# -*- coding: utf-8 -*-
# Odoo, Open Source canet Screen.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).#

import odoo
from odoo import fields, models, api, _

# new fields
class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    is_created = fields.Boolean('Is Created Lot details ?', default=False)