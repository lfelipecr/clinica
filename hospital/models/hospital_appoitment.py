from odoo import models, fields, api, _

states = [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancelled', 'Cancelled')]


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Appointment'
    _order = 'create_date desc'

    name = fields.Char(string='Name', default="New", readonly=True)
    patient_id = fields.Many2one(comodel_name='hospital.patient', string='Patient', required=True)
    patient_age = fields.Integer(string='Age', related="patient_id.age", store=True)
    doctor_id = fields.Many2one(comodel_name='hospital.doctor', string='Doctor', required=True, tracking=True)
    date = fields.Datetime(string='Fecha', required=True, tracking=True)
    state = fields.Selection(string='Estado', selection=states, default='draft')

     # Campo agregado
    consultation_type_id = fields.Many2one(
        'hospital.consultation.type',
        string='Tipo de Consulta',
        required=True,
        help='Selecciona el tipo de consulta asociada a esta cita.'  # Ayuda para el usuario
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _("New")
        result = super(HospitalAppointment, self).create(vals_list)
        return result

    def action_confirm(self):
        self.state = 'confirmed'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancelled'
