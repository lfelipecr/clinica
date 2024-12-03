from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Cita(models.Model):
    _name = 'clinica.cita'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Citas Médicas'

    name = fields.Char(
        string='Referencia', 
        required=True, 
        copy=False, 
        readonly=True, 
        default='Nuevo'
    )
    paciente_id = fields.Many2one(
        'clinica.paciente', 
        string='Paciente', 
        required=True, 
        help='Seleccione el paciente para esta cita.'
    )
    especialidad_id = fields.Many2one(
        'clinica.especialidad', 
        string='Especialidad', 
        required=True, 
        help='Seleccione la especialidad.'
    )
    medico_id = fields.Many2one(
        'clinica.medico', 
        string='Médico', 
        required=True, 
        help='Seleccione el médico asociado a la especialidad seleccionada.',
        domain="[('id', 'in', available_medicos_ids)]"
    )
    fecha_cita = fields.Datetime(
        string='Fecha y Hora', 
        required=True, 
        help='Seleccione la fecha y hora de la cita.'
    )
    estado = fields.Selection(
        [
            ('draft', 'Borrador'), 
            ('confirm', 'Confirmado'), 
            ('done', 'Realizado'), 
            ('cancel', 'Cancelado')
        ],
        string='Estado',
        default='draft',
        tracking=True,
    )
    available_medicos_ids = fields.Many2many(
        'clinica.medico', 
        compute='_compute_available_medicos', 
        string='Médicos Disponibles', 
        help='Médicos asociados a la especialidad seleccionada.'
    )
    notes = fields.Text(string='Notas Adicionales')

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('clinica.cita') or 'Nuevo'
        return super(Cita, self).create(vals)

    @api.depends('especialidad_id')
    def _compute_available_medicos(self):
        for record in self:
            if record.especialidad_id:
                record.available_medicos_ids = record.especialidad_id.medico_ids
            else:
                record.available_medicos_ids = self.env['clinica.medico'].browse()

    @api.constrains('fecha_cita')
    def _check_fecha_cita(self):
        for record in self:
            if record.fecha_cita < fields.Datetime.now():
                raise ValidationError('La fecha de la cita no puede ser en el pasado.')

    def action_confirm(self):
        for record in self:
            if record.estado != 'draft':
                raise ValidationError('Solo puedes confirmar citas en estado borrador.')
            record.estado = 'confirm'

    def action_done(self):
        for record in self:
            if record.estado != 'confirm':
                raise ValidationError('Solo puedes marcar como realizadas citas confirmadas.')
            record.estado = 'done'

    def action_cancel(self):
        for record in self:
            if record.estado == 'done':
                raise ValidationError('No puedes cancelar citas ya realizadas.')
            record.estado = 'cancel'
