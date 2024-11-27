from odoo import models, fields, api, _

class HospitalConsultation(models.Model):
    _name = 'hospital.consultation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Consultation'

    name = fields.Char(string='Reference', required=True, default='New', readonly=True, tracking=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, tracking=True)
    patient_phone = fields.Char(related='patient_id.phone', string='Patient Phone', readonly=True)
    patient_email = fields.Char(related='patient_id.email', string='Patient Email', readonly=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True, tracking=True)
    consultation_type_id = fields.Many2one('hospital.consultation.type', string='Tipo de Consulta', required=True)  # Nuevo campo agregado
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment', required=False)
    date = fields.Datetime(string='Consultation Date', required=True, default=fields.Datetime.now, tracking=True)
    notes = fields.Text(string='Consultation Notes')
    prescription_ids = fields.One2many('hospital.prescription', 'consultation_id', string='Prescripción')
    reason = fields.Char(string='Motivo', required=True, tracking=True)
    consultation_type_id = fields.Many2one(
        'hospital.consultation.type', 
        string='Especialidad',  # Cambiado para reflejar la especialidad
        required=True,
        help='Especialidad asociada a esta consulta.'
    )    

    weight = fields.Float(string='Peso (kg)', help='Peso del paciente en el momento de la consulta.')
    height = fields.Float(string='Altura (cm)', help='Altura del paciente en el momento de la consulta.')
    temperature = fields.Float(string='Temperatura (°C)', help='Temperatura corporal del paciente.')
    blood_pressure = fields.Char(string='Presión Arterial', help='Medición de la presión arterial, e.g., 120/80.')
    heart_rate = fields.Integer(string='Frecuencia Cardíaca (lat/min)', help='Frecuencia cardíaca en latidos por minuto.')
    respiratory_rate = fields.Integer(string='Frecuencia Respiratoria (resp/min)', help='Frecuencia respiratoria en respiraciones por minuto.')
    oxygen_saturation = fields.Float(string='Saturación de Oxígeno (%)', help='Nivel de saturación de oxígeno en la sangre.')  # Campo agregado

    exam_ids = fields.One2many('hospital.exam', 'consultation_id', string='Exámenes')



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('hospital.consultation') or _("New")
        return super(HospitalConsultation, self).create(vals_list)

