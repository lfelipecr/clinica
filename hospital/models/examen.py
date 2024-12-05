from odoo import models, fields, api  # Importación completa

class Examen(models.Model):
    _name = 'clinica.examen'
    _description = 'Examen Médico'

    name = fields.Char(string='Consecutivo', required=True, copy=False, readonly=True, default='Nuevo')
    tipo_examen = fields.Selection([
        ('laboratorio', 'Laboratorio'),
        ('imagen', 'Imagenología'),
        ('otros', 'Otros'),
    ], string='Tipo de Examen', required=True)
    notas = fields.Text(string='Notas')
    fecha_solicitud = fields.Datetime(string='Fecha de Solicitud', default=fields.Datetime.now)
    consulta_id = fields.Many2one('clinica.consulta', string='Consulta', help='Consulta asociada, si aplica.')
    medico_id = fields.Many2one('clinica.medico', string='Médico', help='Médico que solicitó el examen.')
    fecha_realizacion = fields.Datetime(string='Fecha de Realización')
    resultado = fields.Text(string='Resultado')
    archivo_resultado = fields.Binary(string='Archivo Adjunto', attachment=True)
    archivo_nombre = fields.Char(string='Nombre del Archivo')

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('clinica.examen') or 'Nuevo'
        return super(Examen, self).create(vals)
