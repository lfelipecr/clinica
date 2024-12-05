from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Consulta(models.Model):
    _name = 'clinica.consulta'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Consultas Médicas'
    _rec_name = 'name'  # Usar el campo 'name' como identificador principal
    _check_company_auto = True


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
        help='Seleccione el paciente para esta consulta.'
    )
    phone = fields.Char(
        related='paciente_id.phone',
        string='Teléfono',
        readonly=True
    )
    email = fields.Char(
        related='paciente_id.email',
        string='Correo',
        readonly=True
    )
    age = fields.Integer(
        related='paciente_id.age',
        string='Edad',
        readonly=True
    )
    fecha_consulta = fields.Datetime(
        string='Fecha de la Consulta',
        required=True,
        default=fields.Datetime.now,
        help='Indique la fecha y hora de la consulta.'
    )
    motivo = fields.Text(
        string='Motivo',
        required=True,
        help='Describa el motivo de la consulta.'
    )
    cita_id = fields.Many2one(
        'clinica.cita',
        string='Cita Asociada',
        help='Seleccione la cita asociada, si aplica.'
    )
    especialidad_id = fields.Many2one(
        'clinica.especialidad',
        string='Especialidad',
        compute='_compute_especialidad_id',
        store=True,
        help='Especialidad de la consulta. Si está asociada a una cita, será la misma.'
    )
    medico_id = fields.Many2one(
        'clinica.medico',
        string='Médico',
        compute='_compute_medico_id',
        store=True,
        readonly=False,
        help='Médico que atiende esta consulta. Si hay una cita asociada, será el mismo médico de la cita.'
    )
    notas = fields.Text(
        string='Notas',
        help='Notas adicionales sobre la consulta.'
    )
    company_id = fields.Many2one(
        'res.company',
        string='Compañía',
        default=lambda self: self.env.company,
        required=True,
        help='Compañía asociada a esta consulta.'
    )

    # Campos relacionados con información del paciente
    hipertenso = fields.Boolean(
        string='¿Hipertenso?',
        readonly=True
    )
    diabetico = fields.Boolean(
        string='¿Diabético?',
        readonly=True
    )
    peso = fields.Integer(
        string='Peso (kg)',
        help='Indique el peso del paciente. Si se modifica, se actualizará en la ficha del paciente.'
    )
    imc = fields.Float(
        string='IMC',
        compute='_compute_imc',
        store=True,
        help='Índice de Masa Corporal basado en peso y altura.'
    )
    tipo_sangre = fields.Selection(
        selection=[
            ('o_negativo', 'O-'),
            ('o_positivo', 'O+'),
            ('a_negativo', 'A-'),
            ('a_positivo', 'A+'),
            ('b_negativo', 'B-'),
            ('b_positivo', 'B+'),
            ('ab_negativo', 'AB-'),
            ('ab_positivo', 'AB+')
        ],
        string='Tipo de Sangre',
        help='Indique el tipo de sangre. Si se modifica, se actualizará en la ficha del paciente.'
    )
    alergias = fields.Char(
        string='Alergias',
        help='Indique si el paciente tiene alergias conocidas. Si se modifica, se actualizará en la ficha del paciente.'
    )

    temperatura = fields.Float(string='Temperatura (°C)', help='Temperatura del paciente.')
    presion_sanguinea = fields.Char(string='Presión Sanguínea', help='Ejemplo: 120/80')
    nivel_oxigeno = fields.Float(string='Nivel de Oxígeno (%)', help='Nivel de oxígeno en sangre.')
    glicemia = fields.Float(string='Glicemia (mg/dL)', help='Nivel de azúcar en sangre.')
    receta_ids = fields.One2many('clinica.receta', 'consulta_id', string='Recetas')


    @api.onchange('paciente_id')
    def _onchange_paciente_id(self):
        for record in self:
            if record.paciente_id:
                record.hipertenso = record.paciente_id.hipertenso
                record.diabetico = record.paciente_id.diabetico
                record.peso = record.paciente_id.peso
                record.tipo_sangre = record.paciente_id.tipo_sangre
                record.alergias = record.paciente_id.alergias

    @api.depends('cita_id')
    def _compute_especialidad_id(self):
        for record in self:
            record.especialidad_id = record.cita_id.especialidad_id if record.cita_id else False

    @api.depends('cita_id')
    def _compute_medico_id(self):
        for record in self:
            record.medico_id = record.cita_id.medico_id if record.cita_id else False

    @api.depends('peso', 'paciente_id.altura')
    def _compute_imc(self):
        for record in self:
            if record.peso and record.paciente_id.altura:
                altura_metros = record.paciente_id.altura / 100.0
                record.imc = record.peso / (altura_metros ** 2)
            else:
                record.imc = 0

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('clinica.consulta') or 'Nuevo'
        consulta = super(Consulta, self).create(vals)
        consulta._update_paciente_fields()
        return consulta

    def write(self, vals):
        res = super(Consulta, self).write(vals)
        self._update_paciente_fields()
        return res

    def _update_paciente_fields(self):
        for record in self:
            if record.peso:
                record.paciente_id.peso = record.peso
            if record.imc:
                record.paciente_id.imc = record.imc
            if record.tipo_sangre:
                record.paciente_id.tipo_sangre = record.tipo_sangre
            if record.alergias:
                record.paciente_id.alergias = record.alergias

    @api.constrains('fecha_consulta')
    def _check_fecha_consulta(self):
        for record in self:
            if record.fecha_consulta > fields.Datetime.now():
                raise ValidationError('La fecha de la consulta no puede estar en el futuro.')
