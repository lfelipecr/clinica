from odoo import models, fields, api, _
from datetime import date  # Importar `date` del módulo `datetime`

# Opciones para los campos de selección
VACUNAS_OPTIONS = [
    ('bcg', 'BCG (Tuberculosis)'),
    ('hepatitis_b', 'Hepatitis B'),
    ('pentavalente', 'Pentavalente (Difteria, Tosferina, Tétanos, Hepatitis B, Haemophilus Influenzae tipo B)'),
    ('rotavirus', 'Rotavirus'),
    ('neumococo', 'Neumococo'),
    ('influenza', 'Influenza'),
    ('sarampion_rubeola', 'Sarampión y Rubéola'),
    ('dpt', 'DPT (Difteria, Tosferina y Tétanos)'),
    ('poliomielitis', 'Poliomielitis'),
    ('vph', 'Virus del Papiloma Humano (VPH)'),
    ('covid19', 'COVID-19'),
]

TIPO_SANGRE_OPTIONS = [
    ('o_negativo', 'O-'),
    ('o_positivo', 'O+'),
    ('a_negativo', 'A-'),
    ('a_positivo', 'A+'),
    ('b_negativo', 'B-'),
    ('b_positivo', 'B+'),
    ('ab_negativo', 'AB-'),
    ('ab_positivo', 'AB+'),
]

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']  # Mantener para funcionalidad del Chatter y portal
    _rec_name = 'contact_id'  # Usar el campo 'contact_id' como representación
    _description = 'Patients'

    # Campos principales
    sequence = fields.Char(string='Sequence', default="New", readonly=True)  # Secuencia única para cada paciente
    contact_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contacto',
        ondelete='set null',
        help='Selecciona el contacto asociado a este paciente.'
    )
    phone = fields.Char(related='contact_id.phone', string='Teléfono', readonly=True)  # Teléfono del contacto relacionado
    email = fields.Char(related='contact_id.email', string='Correo Electrónico', readonly=True)  # Email del contacto relacionado
    nacimiento = fields.Date(string='Fecha de Nacimiento', required=False, tracking=True)  # Fecha de nacimiento del paciente
    age = fields.Integer(string='Edad', compute='_compute_age', store=False, tracking=True)  # Cálculo automático de la edad
    gender = fields.Selection(
        string='Género',
        selection=[('male', 'Masculino'), ('female', 'Femenino')],
        default='male',
        tracking=True
    )
    peso = fields.Integer(string='Peso (kg)', required=False, tracking=True)  # Peso del paciente en kg
    altura = fields.Integer(string='Altura (cm)', required=False, tracking=True)  # Altura del paciente en cm
    imc = fields.Float(string='IMC', compute='_compute_imc', store=True, readonly=True)  # Cálculo del IMC basado en peso y altura
    diabetico = fields.Boolean(string='¿Es diabético?')  # AGREGADO: Campo para indicar si es diabético
    hipertenso = fields.Boolean(string='¿Es hipertenso?')  # AGREGADO: Campo para indicar si es hipertenso
    # Campos adicionales
    vacunas = fields.Selection(
        selection=VACUNAS_OPTIONS,
        string='Vacunas',
        help='Selecciona una vacuna del esquema de vacunación.'
    )
    tipo_sangre = fields.Selection(
        selection=TIPO_SANGRE_OPTIONS,
        string='Tipo de Sangre',
        help='Selecciona el tipo de sangre del paciente.'
    )
    antecedentes_personales = fields.Text(string='Antecedentes Personales')  # Información sobre antecedentes personales
    medicamentos_actuales = fields.Many2many(comodel_name='product.product', string='Medicamentos Actuales')  # Relación con medicamentos
    fuma = fields.Boolean(string='Fuma')  # Indicador de si el paciente fuma
    alcohol = fields.Boolean(string='Consumo de Alcohol')  # Indicador de consumo de alcohol
    drogas = fields.Boolean(string='Uso de Drogas')  # Indicador de consumo de drogas
    cocina_lena = fields.Boolean(string='¿Usa cocina de leña?')  # Indicador de uso de cocina de leña
    antecedentes_heredofamiliares = fields.Text(string='Antecedentes Heredofamiliares')  # Información sobre antecedentes familiares
    alergias = fields.Char(string='Alergias', help='Indica si el paciente tiene alguna alergia conocida.')  # Alergias del paciente
    antecedentes_quirurgicos = fields.Text(string='Antecedentes Quirúrgicos')  # Información sobre cirugías previas
    sexualmente_activo = fields.Boolean(string='Sexualmente Activo')  # Indicador de actividad sexual
    metodo_planificacion = fields.Selection(
        string='Método de Planificación',
        selection=[
            ('pildora', 'Píldora'),
            ('inyeccion', 'Inyección'),
            ('t_cobre', 'T-Cobre'),
            ('ritmo', 'Ritmo'),
            ('condon', 'Condón'),
            ('ninguno', 'Ninguno')
        ],
        default='ninguno'
    )
    numero_embarazos = fields.Integer(string='Número de Embarazos', required=False)
    numero_partos = fields.Integer(string='Número de Partos', required=False)
    numero_abortos = fields.Integer(string='Número de Abortos', required=False)
    numero_cesareas = fields.Integer(string='Número de Cesáreas', required=False)
    fecha_ultima_citologia = fields.Date(string='Fecha de Última Citología')

    # Control de visibilidad de pestañas
    show_ginecologicos = fields.Boolean(
        string="Mostrar Pestaña Ginecológicos",
        compute="_compute_show_ginecologicos",
        store=False
    )

    consultation_count = fields.Integer(
        string='Consultas',
        compute='_compute_consultation_count',
        store=False
    )  # Campo computado para contar consultas

    # Campo computado para contar citas
    appointment_count = fields.Integer(
        string='Citas',
        compute='_compute_appointment_count',
        store=False
    )
    
    # Campo computado para el monto total facturado
    total_invoiced = fields.Monetary(
        string='Monto Facturado',
        compute='_compute_total_invoiced',
        currency_field='currency_id',
        store=False
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id,
        required=True
    )

     
    # Campos para el Chatter (Agregados)
    message_follower_ids = fields.One2many(
        'mail.followers', 'res_id',
        string='Followers',
        auto_join=True,
        readonly=True
    )
    message_ids = fields.One2many(
        'mail.message', 'res_id',
        string='Messages',
        auto_join=True,
        readonly=True
    )
    activity_ids = fields.One2many(
        'mail.activity', 'res_id',
        string='Activities',
        auto_join=True,
        readonly=True
    )


    # Métodos para cálculos
    @api.depends('nacimiento')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.nacimiento:
                record.age = today.year - record.nacimiento.year - (
                    (today.month, today.day) < (record.nacimiento.month, record.nacimiento.day)
                )
            else:
                record.age = 0

    @api.depends('peso', 'altura')
    def _compute_imc(self):
        for record in self:
            if record.peso and record.altura:
                altura_metros = record.altura / 100.0
                record.imc = record.peso / (altura_metros ** 2)
            else:
                record.imc = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('sequence', _("New")) == _("New"):
                vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _("New")
        result = super(HospitalPatient, self).create(vals_list)
        return result

    @api.depends('gender')
    def _compute_show_ginecologicos(self):
        for record in self:
            record.show_ginecologicos = record.gender == 'female'
    
    def _compute_consultation_count(self):
        for record in self:
            record.consultation_count = self.env['hospital.consultation'].search_count([
                ('patient_id', '=', record.id)
            ])  # Cuenta las consultas asociadas al paciente

    def action_view_consultations(self):
        """Acción para mostrar las consultas del paciente."""
        return {
            'name': _('Consultas'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.consultation',
            'domain': [('patient_id', '=', self.id)],
            'context': dict(self.env.context, default_patient_id=self.id),
        }
    
    def _compute_appointment_count(self):
        for record in self:
            record.appointment_count = self.env['hospital.appointment'].search_count([
                ('patient_id', '=', record.id)
            ])  # Cuenta las citas asociadas al paciente

    def action_view_appointments(self):
        """Acción para mostrar las citas del paciente."""
        return {
            'name': _('Citas'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointment',
            'domain': [('patient_id', '=', self.id)],
            'context': dict(self.env.context, default_patient_id=self.id),
        }

    def _compute_total_invoiced(self):
        for record in self:
            invoices = self.env['account.move'].search([
                ('partner_id', '=', record.contact_id.id),
                ('state', '=', 'posted'),
                ('move_type', '=', 'out_invoice')  # Solo facturas de cliente
            ])
            record.total_invoiced = sum(invoices.mapped('amount_total'))  # Suma el total de las facturas

    def action_view_invoices(self):
        """Acción para mostrar las facturas del paciente."""
        return {
            'name': _('Facturas'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [
                ('partner_id', '=', self.contact_id.id),
                ('state', '=', 'posted'),
                ('move_type', '=', 'out_invoice')
            ],
            'context': dict(self.env.context, default_partner_id=self.contact_id.id),
        }
    
