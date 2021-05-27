# -*- coding: utf-8 -*-
# Odoo, Open Source canet Screen.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).# 

from odoo import fields, models, api, _
from odoo.exceptions import UserError
    
# new fields 
class StockInventory(models.Model):
    _inherit = 'stock.inventory'
     
    user_id = fields.Many2one('res.users', 'Responsible')
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.inventory') or _('New')
        result = super(StockInventory, self).create(vals)
        return result
    
    
    # write the product in lot id
    def action_done(self):
        sample_product_id = self.env.ref('canet_screen.sample_product_canet_id').id
        for line in self.line_ids :
            if line.prod_lot_id :
                if line.prod_lot_id.product_id.id == sample_product_id :
                    line.prod_lot_id.write({'product_id' : line.product_id.id})
        negative = next((line for line in self.mapped('line_ids') if line.product_qty < 0 and line.product_qty != line.theoretical_qty), False)
        if negative:
            raise UserError(_('You cannot set a negative product quantity in an inventory line:\n\t%s - qty: %s') % (negative.product_id.name, negative.product_qty))
        self.action_check()
        self.write({'state': 'done'})
        self.post_inventory()
        
        return True

    def _get_inventory_lines_values(self):
        # TDE CLEANME: is sql really necessary ? I don't think so
        locations = self.env['stock.location'].search([('id', 'child_of', [self.location_id.id])])
        domain = ' location_id in %s AND active = TRUE'
        args = (tuple(locations.ids),)

        vals = []
        Product = self.env['product.product']
        # Empty recordset of products available in stock_quants
        quant_products = self.env['product.product']
        # Empty recordset of products to filter
        products_to_filter = self.env['product.product']

        # case 0: Filter on company
        if self.company_id:
            domain += ' AND company_id = %s'
            args += (self.company_id.id,)

        # case 1: Filter on One owner only or One product for a specific owner
        if self.partner_id:
            domain += ' AND owner_id = %s'
            args += (self.partner_id.id,)
        # case 2: Filter on One Lot/Serial Number
        if self.lot_id:
            domain += ' AND lot_id = %s'
            args += (self.lot_id.id,)
        # case 3: Filter on One product
        if self.product_id:
            domain += ' AND product_id = %s'
            args += (self.product_id.id,)
            products_to_filter |= self.product_id
        # case 4: Filter on A Pack
        if self.package_id:
            domain += ' AND package_id = %s'
            args += (self.package_id.id,)
        # case 5: Filter on One product category + Exahausted Products
        if self.category_id:
            categ_products = Product.search([('categ_id', '=', self.category_id.id)])
            domain += ' AND product_id = ANY (%s)'
            args += (categ_products.ids,)
            products_to_filter |= categ_products

        self.env.cr.execute("""SELECT product_id, sum(quantity) as product_qty, location_id, lot_id as prod_lot_id, package_id, owner_id as partner_id
            FROM stock_quant
            LEFT JOIN product_product
            ON product_product.id = stock_quant.product_id
            WHERE %s
            GROUP BY product_id, location_id, lot_id, package_id, partner_id """ % domain, args)
        lot_obj = self.env['stock.production.lot']
        for product_data in self.env.cr.dictfetchall():
            # replace the None the dictionary by False, because falsy values are tested later on
            for void_field in [item[0] for item in product_data.items() if item[1] is None]:
                product_data[void_field] = False
            product_data['theoretical_qty'] = product_data['product_qty']
            if product_data['product_id']:
                product_data['product_uom_id'] = Product.browse(product_data['product_id']).uom_id.id
                quant_products |= Product.browse(product_data['product_id'])
                Product = Product.browse(product_data['product_id'])
                if Product.barcode:
                    product_data['barcode'] = Product.barcode
                    # lot_ids = lot_obj.search([('name', '=', Product.barcode)])
                    # if not lot_ids:
                    #     val = {
                    #         'name': Product.barcode,
                    #         'product_id': Product.id,
                    #     }
                    #     create_lot_id = lot_obj.sudo().create(val)
                    #     product_data['prod_lot_id'] = int(create_lot_id[0].id)
                    # else:
                    #     product_data['prod_lot_id'] = int(lot_ids[0].id)
            vals.append(product_data)
        if self.exhausted:
            exhausted_vals = self._get_exhausted_inventory_line(products_to_filter, quant_products)
            vals.extend(exhausted_vals)
        return vals

    def _get_exhausted_inventory_line(self, products, quant_products):
        '''
        This function return inventory lines for exausted products
        :param products: products With Selected Filter.
        :param quant_products: products available in stock_quants
        '''
        vals = []
        prod_lot_id = False
        exhausted_domain = [('type', 'not in', ('service', 'consu', 'digital'))]
        if products:
            exhausted_products = products - quant_products
            exhausted_domain += [('id', 'in', exhausted_products.ids)]
        else:
            exhausted_domain += [('id', 'not in', quant_products.ids)]
        exhausted_products = self.env['product.product'].search(exhausted_domain)
        for product in exhausted_products:
            # if product.barcode:
            #     lot_ids = lot_obj.search([('name', '=', product.barcode)])
            #     print("<<<<<<<<<<<crelot_ids<<", lot_ids[0].id)
            #     if not lot_ids:
            #         val = {
            #             'name': product.barcode,
            #             'product_id': product.id,
            #         }
            #         create_lot_id = lot_obj.sudo().create(val)
            #
            #         prod_lot_id = int(create_lot_id[0].id)
            #     else:
            #         prod_lot_id=  int(lot_ids[0].id)
            vals.append({
                'inventory_id': self.id,
                'product_id': product.id,
                'barcode': product.barocde,
                'location_id': self.location_id.id,
            })
        print ("<<<<<<<<<<<<<<<<",vals)
        return vals
    
    
# change prod_lot_id domain     
class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    sample_product_id = fields.Many2one(
        'product.product', 'Sample_product'
        )
    prod_lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number'
        )
    barcode = fields.Char('Barcode')
    
    # set the sample product
    @api.model
    def default_get(self, vals):
        res = super(InventoryLine, self).default_get(vals)
        ctx = dict(self._context)
        if 'default_filter' in ctx :
            if ctx.get('default_filter') == 'none' :
                res.update({'sample_product_id': self.env.ref('canet_screen.sample_product_canet_id').id})
        return res

    @api.onchange('product_id')
    def onchange_product(self):
        res = {}
        # If no UoM or incorrect UoM put default one from product
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id
            lot_obj = self.env['stock.production.lot']
            res['domain'] = {'product_uom_id': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
            if self.product_id.barcode:
                # lot_ids = lot_obj.search([('name','=',self.product_id.barcode )])
                # if not lot_ids:
                #     vals = {
                #         'name': self.product_id.barcode,
                #         'product_id': self.product_id.id,
                #     }
                #     create_lot_id = lot_obj.sudo().create(vals)
                self.barcode = self.product_id.barcode
        return res
