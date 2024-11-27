from odoo import models, fields, api, _
from datetime import date

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Doctor'

    name = fields.Char(string="Nombre", required=True, tracking=True)
    age = fields.Integer(string='Edad', compute='_compute_age', store=True, tracking=True, help="La edad se calcula automáticamente a partir de la fecha de nacimiento.")
    gender = fields.Selection(
        string='Género',
        selection=[('male', 'Masculino'), ('female', 'Femenino')],
        default='male',
        tracking=True
    )
    specialty_id = fields.Many2one(
        'hospital.consultation.type',
        string='Especialidad',
        required=True,
        tracking=True,
        help="Especialidad del doctor asociada al modelo de tipos de consulta."
    )
    photo = fields.Image(
        string='Foto',
        max_width=512,
        max_height=512,
        help="Foto del doctor"
    )
    birth_date = fields.Date(
        string='Fecha de Nacimiento',
        required=False,
        help="Fecha de nacimiento del doctor"
    )
    medical_card = fields.Char(
        string='Carné de Médico',
        required=True,
        help="Número de carné profesional del médico."
    )
    medical_school = fields.Char(
        string='Escuela de Medicina',
        required=True,
        help="Institución donde el doctor obtuvo su título."
    )
    id_number = fields.Char(
        string='Número de Identificación',
        required=True,
        help="Número de identificación oficial del doctor."
    )
    id_type = fields.Selection(
        [
            ('cedula_identidad', 'Cédula de Identidad'),
            ('cedula_residencia', 'Cédula de Residencia'),
            ('dimex', 'DIMEX')
        ],
        string='Tipo de Identificación',
        required=True,
        help="Tipo de identificación oficial del doctor."
    )

    @api.depends('birth_date')
    def _compute_age(self):
        """
        Calcula la edad automáticamente en base a la fecha de nacimiento.
        """
        for record in self:
            if record.birth_date:
                today = date.today()
                birth_date = record.birth_date
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.age = age
            else:
                record.age = 0
