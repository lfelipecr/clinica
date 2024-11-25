from odoo import models, fields, _
class HospitalExamType(models.Model):
    _name = 'hospital.exam.type'
    _description = 'Tipo de Examen'

    name = fields.Char(string='Nombre del Examen', required=True, help='Nombre del tipo de examen.')
    description = fields.Text(string='Descripción', help='Descripción del tipo de examen.')
    code = fields.Char(string='Código', help='Código único para el tipo de examen.')
