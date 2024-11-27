from odoo import models, fields, api

class HospitalExam(models.Model):
    _name = 'hospital.exam'
    _description = 'Exámenes'

    request_date = fields.Datetime(
        string='Fecha de Solicitud',
        default=fields.Datetime.now,
        required=True
    )
    exam_type_id = fields.Many2one(
        'hospital.exam.type',
        string='Tipo de Examen',
        required=True
    )
    priority = fields.Selection(
        [
            ('low', 'Baja'),
            ('normal', 'Normal'),
            ('high', 'Alta'),
        ],
        string='Prioridad',
        default='normal',
        required=True
    )
    notes = fields.Text(string='Notas')
    results = fields.Text(string='Resultados')
    done_date = fields.Datetime(string='Fecha de Realización')
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Adjuntos'
    )
    patient_id = fields.Many2one(
        'hospital.patient',
        string='Paciente',
        ondelete='cascade',
        required=False,  # No obligatorio para permitir creación independiente
        help='Paciente asociado al examen.'
    )
    consultation_id = fields.Many2one(
        'hospital.consultation',
        string='Consulta',
        ondelete='set null',
        help='Consulta asociada al examen, si aplica.'
    )
    doctor_id = fields.Many2one(
        'hospital.doctor', 
        string='Doctor Solicitante', 
        ondelete='set null',
        help='Doctor que solicitó el examen.'
    )

    @api.onchange('consultation_id')
    def _onchange_consultation_id(self):
        """
        Al cambiar la consulta, se asigna automáticamente el paciente relacionado con la consulta.
        """
        for record in self:
            if record.consultation_id:
                record.patient_id = record.consultation_id.patient_id

    @api.model_create_multi
    def create(self, vals_list):
        """
        Asigna automáticamente el paciente desde la consulta, si está presente.
        """
        for vals in vals_list:
            consultation_id = vals.get('consultation_id')
            if consultation_id:
                consultation = self.env['hospital.consultation'].browse(consultation_id)
                vals['patient_id'] = consultation.patient_id.id
        return super(HospitalExam, self).create(vals_list)
