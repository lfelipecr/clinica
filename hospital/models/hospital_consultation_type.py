from odoo import models, fields, _

class HospitalConsultationType(models.Model):
    _name = 'hospital.consultation.type'
    _description = 'Consultation Type'

    # Campo obligatorio para el nombre del tipo de consulta
    name = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre del tipo de consulta'
    )
    
    # Campo opcional para observaciones
    description = fields.Text(
        string='Observaciones',
        help='Observaciones sobre el tipo de consulta'
    )
    
    # Opcional: Agregar un campo de código único para el tipo de consulta
    code = fields.Char(
        string='Código',
        required=False,
        help='Código único para identificar el tipo de consulta'
    )

    doctor_ids = fields.Many2many(
        comodel_name='hospital.doctor',
        relation='hospital_consultation_type_doctor_rel',
        column1='consultation_type_id',
        column2='doctor_id',
        string='Doctores Asociados',
        help='Doctores que pueden realizar este tipo de consulta'
    )  # Campo añadido para asociar doctores
    
    # Campo para la moneda
    currency_id = fields.Many2one(
        'res.currency', 
        string='Moneda',
        required=True, 
        default=lambda self: self.env.company.currency_id,
        help='Moneda para el valor de la consulta.'
    )  # Campo Many2one para seleccionar moneda

    # Campo para el monto de la consulta
    valor = fields.Monetary(
        string='Valor',
        currency_field='currency_id',
        required=True,
        help='Costo de la consulta en la moneda seleccionada.'
    )  # Campo para el monto

    # Campo para asociar un producto facturable
    product_id = fields.Many2one(
        'product.product',
        string='Producto Asociado',
        required=True,
        help='Producto que se facturará cuando se realice este tipo de consulta.'
    )  # Campo Many2one para asociar un producto


    # Opcional: Agregar tracking para mejorar la trazabilidad en el modelo
    _inherit = ['mail.thread', 'mail.activity.mixin']
