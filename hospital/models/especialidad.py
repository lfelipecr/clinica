from odoo import models, fields

class Especialidad(models.Model):
    _name = 'clinica.especialidad'
    _description = 'Especialidades Médicas'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True

    name = fields.Char(string='Nombre de la Especialidad', required=True, tracking=True)
    consultation_cost = fields.Monetary(string='Costo de la Consulta', required=True)
    product_id = fields.Many2one(
        'product.product',
        string='Producto Asociado',
        domain="[('type', '=', 'service')]",
        required=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Compañía',
        default=lambda self: self.env.company,
        required=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    medico_ids = fields.Many2many(
        'clinica.medico',
        string='Médicos Asociados',
        help='Selecciona los médicos que pueden ofrecer esta especialidad.',
    )
