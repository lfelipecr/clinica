from odoo import models, fields, api

class Medico(models.Model):
    _name = 'clinica.medico'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Médicos'
    _check_company_auto = True  # Activa la validación automática de compañía

    name = fields.Many2one(
        'hr.employee',
        string='Médico',
        required=True,
        ondelete='cascade',
        help='Seleccione un empleado que sea un médico.',
    )
    specialty = fields.Char(string='Especialidad', tracking=True)
    license_number = fields.Char(string='Número de Licencia', required=True)
    phone = fields.Char(related='name.work_phone', string='Teléfono', readonly=True)
    email = fields.Char(related='name.work_email', string='Correo Electrónico', readonly=True)
    active = fields.Boolean(string='Activo', default=True)
    consulta_id = fields.Many2one('clinica.consulta', string='Consulta', help='Consulta asociada, si aplica.')


    # Campo de compañía
    company_id = fields.Many2one(
        'res.company',
        string='Compañía',
        default=lambda self: self.env.company,
        required=True,
    )

    _sql_constraints = [
        ('unique_license_number', 'unique(license_number)', 'El número de licencia debe ser único para cada médico.'),
    ]
