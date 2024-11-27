from odoo import models, fields, api, _

class HospitalConsultation(models.Model):
    _name = 'hospital.consultation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Consultation'

    # Campos principales
    name = fields.Char(
        string='Referencia', 
        required=True, 
        default='New', 
        readonly=True, 
        tracking=True
    )
    patient_id = fields.Many2one(
        'hospital.patient', 
        string='Paciente', 
        required=True, 
        tracking=True
    )
    patient_phone = fields.Char(
        related='patient_id.phone', 
        string='Teléfono del Paciente', 
        readonly=True
    )
    patient_email = fields.Char(
        related='patient_id.email', 
        string='Correo del Paciente', 
        readonly=True
    )
    doctor_id = fields.Many2one(
        'hospital.doctor', 
        string='Doctor', 
        required=True, 
        tracking=True
    )
    consultation_type_id = fields.Many2one(
        'hospital.consultation.type', 
        string='Especialidad', 
        required=True,
        help='Especialidad asociada a esta consulta.'
    )
    appointment_id = fields.Many2one(
        'hospital.appointment', 
        string='Cita Asociada', 
        required=False
    )
    date = fields.Datetime(
        string='Fecha de la Consulta', 
        required=True, 
        default=fields.Datetime.now, 
        tracking=True
    )
    notes = fields.Text(
        string='Notas de la Consulta'
    )
    prescription_ids = fields.One2many(
        'hospital.prescription', 
        'consultation_id', 
        string='Prescripciones'
    )
    reason = fields.Char(
        string='Motivo Consulta', 
        tracking=True
    )
    weight = fields.Float(
        string='Peso (kg)', 
        help='Peso del paciente en el momento de la consulta.'
    )
    height = fields.Float(
        string='Altura (cm)', 
        help='Altura del paciente en el momento de la consulta.'
    )
    temperature = fields.Float(
        string='Temperatura (°C)', 
        help='Temperatura corporal del paciente.'
    )
    blood_pressure = fields.Char(
        string='Presión Arterial', 
        help='Medición de la presión arterial, e.g., 120/80.'
    )
    heart_rate = fields.Integer(
        string='Frecuencia Cardíaca (lat/min)', 
        help='Frecuencia cardíaca en latidos por minuto.'
    )
    respiratory_rate = fields.Integer(
        string='Frecuencia Respiratoria (resp/min)', 
        help='Frecuencia respiratoria en respiraciones por minuto.'
    )
    oxygen_saturation = fields.Float(
        string='Saturación de Oxígeno (%)', 
        help='Nivel de saturación de oxígeno en la sangre.'
    )
    exam_ids = fields.One2many(
        'hospital.exam', 
        'consultation_id', 
        string='Exámenes'
    )

    # Métodos
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('hospital.consultation') or _("New")
        return super(HospitalConsultation, self).create(vals_list)

    @api.onchange('exam_ids')
    def _onchange_exam_ids(self):
        for exam in self.exam_ids:
            if not exam.patient_id:
                exam.patient_id = self.patient_id
            if not exam.doctor_id:
                exam.doctor_id = self.doctor_id

    def write(self, vals):
        res = super(HospitalConsultation, self).write(vals)
        for exam in self.exam_ids:
            if not exam.patient_id:
                exam.patient_id = self.patient_id
            if not exam.doctor_id:
                exam.doctor_id = self.doctor_id
        return res
