from odoo import models, fields

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
    priority = fields.Selection([
        ('low', 'Baja'),
        ('normal', 'Normal'),
        ('high', 'Alta'),
    ], string='Prioridad', 
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
        ondelete='cascade'
    )
    consultation_id = fields.Many2one(
        'hospital.consultation', 
        string='Consulta', 
        ondelete='set null'
    )
