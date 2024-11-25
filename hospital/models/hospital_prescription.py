from odoo import models, fields, api

class HospitalPrescription(models.Model):
    _name = 'hospital.prescription'
    _description = 'Prescription'

    consultation_id = fields.Many2one('hospital.consultation', string='Consultation', required=True, ondelete='cascade')
    medicine_id = fields.Many2one('product.product', string='Medicine', required=True)
    dosage = fields.Char(string='Dosage')
    duration = fields.Char(string='Duration')
    notes = fields.Text(string='Notes')
