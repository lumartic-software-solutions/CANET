# -*- coding: utf-8 -*-
# Odoo, Open Source Ballester Product.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp

# new fields for teixo documentation


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    uncode = fields.Char('UN Code')
    lercode_id = fields.Many2one('ler.code', 'Ler Code')
    admission_parameters = fields.Char('Admission parameters for DA')
    treatement_operation_ids = fields.Many2many(
        'treatement.operation', 'treatment_product_rel', 'treatment_id', 'product_id', 'Treatment Operation')
    danger_char_ids = fields.Many2many(
        'danger.characteristic', 'danger_product_rel', 'danger_id', 'product_id', 'Danger Characteristics')
    lot_attribute_line_ids = fields.One2many(
        'lot.attribute.line', 'product_tmpl_id', 'Lot Attributes')
    weight = fields.Float(
        'Weight', compute='_compute_weight', digits=dp.get_precision('Stock Weight'),
        inverse='_set_weight', store=True,
        help="The weight of the contents in Kg, not including any packaging, etc.")
    default_code = fields.Char(
        'Internal Reference', compute='_compute_default_code',
        inverse='_set_default_code', store=True)

    # when change the lercode_id it will set the uncode
    @api.onchange('lercode_id')
    def onchange_lercode(self):
        if self.lercode_id:
            if self.lercode_id.dangerous == True:
                self.uncode = 'EMBALAJE VACIO , ,GE III'
            else:
                self.uncode = ''

    @api.depends('product_variant_ids', 'product_variant_ids.default_code')
    def _compute_default_code(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.default_code = template.product_variant_ids.default_code

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        templates = self.env['product.template'].search([])
        if name:
            domain = ['|', '|', ('barcode', 'ilike', name),
                      ('name', 'ilike', name),
                      ('default_code', 'ilike', name)]
            templates = self.search(domain)
        return templates.name_get()


class LerCode(models.Model):
    _name = 'ler.code'

    name = fields.Char('Code')
    description = fields.Char('Description')
    dangerous = fields.Boolean('Dangerous', defualt=False)

    # set name with description
    @api.multi
    def name_get(self):
        return [(value.id, "[%s] %s" % (value.name, value.description)) for value in self]

# treatment Operation


class TretmentOperation(models.Model):
    _name = 'treatement.operation'

    name = fields.Char('Operation')
    description = fields.Char('Description')

    # set name with description
    @api.multi
    def name_get(self):
        return [(value.id, "[%s] %s" % (value.name, value.description)) for value in self]


# danger characteristics
class DangerCharacteristics(models.Model):
    _name = 'danger.characteristic'

    name = fields.Char('Code')
    description = fields.Char('Description')

    # set name with description
    @api.multi
    def name_get(self):
        return [(value.id, "[%s] %s" % (value.name, value.description)) for value in self]
