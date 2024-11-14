from odoo import models, fields, api, _


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Patients'

    name = fields.Char(string='Nombre', required=True, tracking=True)   
    sequence = fields.Char(string='Sequence', default="New", readonly=True)
    age = fields.Integer(string='Edad', required=True, tracking=True)
    gender = fields.Selection(string='Genero', selection=[('male', 'Masculino'), ('female', 'Femenino')], default='male', tracking=True)
    email = fields.Char(string='Correo')
    company_id = fields.Many2one(comodel_name='res.company', default=lambda self: self.env.company)
    contact_id = fields.Many2one(comodel_name='res.partner',string='Contacto',ondelete='set null',help='Selecciona el contacto asociado a este paciente.')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', _("New")) == _("New"):
                vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _("New")
        result = super(HospitalPatient, self).create(vals_list)
        return result
