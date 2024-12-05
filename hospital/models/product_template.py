from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    medicamento = fields.Boolean(string='Es Medicamento', default=False, help='Marque esta casilla si este producto es un medicamento.')
