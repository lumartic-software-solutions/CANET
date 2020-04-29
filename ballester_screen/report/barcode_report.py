# -*- coding: utf-8 -*-
# Odoo, Open Source Ballester Screen.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).# 
                                       
from odoo import api, models


# Barcode reports 
class BarcodeReport(models.AbstractModel):
    _name = 'report.ballester_screen.report_barcode'

    @api.multi
    def get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docargs = {
            'doc_model': 'stock.inventory.line',
            'docs':self.ids,
            'data': data,
        }
        return docargs
