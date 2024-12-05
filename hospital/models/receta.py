from odoo import models, fields, api

class Receta(models.Model):
    _name = 'clinica.receta'
    _description = 'Receta Médica'

    name = fields.Char(string='Referencia', required=True, copy=False, readonly=True, default='Nuevo')
    medico_id = fields.Many2one('clinica.medico', string='Médico', required=True, help='Médico que emite la receta.')
    fecha_emision = fields.Datetime(string='Fecha de Emisión', default=fields.Datetime.now, required=True)
    consulta_id = fields.Many2one('clinica.consulta', string='Consulta', help='Consulta asociada a esta receta (opcional).')
    receta_lineas = fields.One2many('clinica.receta.linea', 'receta_id', string='Líneas de Receta', required=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('clinica.receta') or 'Nuevo'
        return super(Receta, self).create(vals)


class RecetaLinea(models.Model):
    _name = 'clinica.receta.linea'
    _description = 'Línea de Receta'

    receta_id = fields.Many2one('clinica.receta', string='Receta', required=True, ondelete='cascade')
    producto_id = fields.Many2one('product.product', string='Medicamento', required=True, 
                                  domain="[('medicamento', '=', True)]",
                                  help='Seleccione un producto marcado como medicamento.')
    dosis = fields.Char(string='Dosis', required=True, help='Especifica la dosis del medicamento.')
    duracion = fields.Char(string='Duración', required=True, help='Especifica la duración del tratamiento.')
    frecuencia = fields.Char(string='Frecuencia', required=True, help='Ejemplo: Una vez al día, dos veces al día, etc.')
