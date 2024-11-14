from odoo import models, fields, api, _


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Doctor'

    name = fields.Char(string="Nombre", required=True, tracking=True)
    age = fields.Integer(string='Edad', required=True, tracking=True)
    gender = fields.Selection(string='Genero', selection=[('male', 'Masculino'), ('female', 'Femenino')], default='male')
    specialty = fields.Char(string='Specialidad', required=True, tracking=True)
