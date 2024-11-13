from odoo import models, fields, api, _


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Doctor'

    name = fields.Char(string="Name", required=True, tracking=True)
    age = fields.Integer(string='Age', required=True, tracking=True)
    gender = fields.Selection(string='Gender', selection=[('male', 'Male'), ('female', 'Female')], default='male')
    specialty = fields.Char(string='Specialty', required=True, tracking=True)
