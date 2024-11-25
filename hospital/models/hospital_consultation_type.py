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



    # Opcional: Agregar tracking para mejorar la trazabilidad en el modelo
    _inherit = ['mail.thread', 'mail.activity.mixin']
