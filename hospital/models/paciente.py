from odoo import models, fields, api, _
from datetime import date

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
    _name = 'clinica.paciente'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _rec_name = 'contact_id'
    _description = 'Pacientes'

    # Activar multicompañía automáticamente para que respete el campo company_id
    _check_company_auto = True


    sequence = fields.Char(string='Sequence', default="New", readonly=True)
    contact_id = fields.Many2one('res.partner', string='Contacto', ondelete='set null', help='Selecciona el contacto asociado a este paciente.')
    phone = fields.Char(related='contact_id.mobile', string='Celular', readonly=True)
    email = fields.Char(related='contact_id.email', string='Correo Electrónico', readonly=True)
    nacimiento = fields.Date(string='Fecha de Nacimiento', required=False, tracking=True)
    age = fields.Integer(string='Edad', compute='_compute_age', store=False, tracking=True)
    gender = fields.Selection([('male', 'Masculino'), ('female', 'Femenino')], string='Género', default='male', tracking=True)
    peso = fields.Integer(string='Peso (kg)', required=False, tracking=True)
    altura = fields.Integer(string='Altura (cm)', required=False, tracking=True)
    imc = fields.Float(string='IMC', compute='_compute_imc', store=True, readonly=True)
    diabetico = fields.Boolean(string='¿Es diabético?')
    hipertenso = fields.Boolean(string='¿Es hipertenso?')
    vacunas = fields.Selection(selection=VACUNAS_OPTIONS, string='Vacunas', help='Selecciona una vacuna del esquema de vacunación.')
    tipo_sangre = fields.Selection(selection=TIPO_SANGRE_OPTIONS, string='Tipo de Sangre', help='Selecciona el tipo de sangre del paciente.')
    antecedentes_personales = fields.Text(string='Antecedentes Personales')
    medicamentos_actuales = fields.Many2many('product.product', string='Medicamentos Actuales')
    fuma = fields.Boolean(string='Fuma')
    alcohol = fields.Boolean(string='Consumo de Alcohol')
    drogas = fields.Boolean(string='Uso de Drogas')
    cocina_lena = fields.Boolean(string='¿Usa cocina de leña?')
    antecedentes_heredofamiliares = fields.Text(string='Antecedentes Heredofamiliares')
    alergias = fields.Char(string='Alergias', help='Indica si el paciente tiene alguna alergia conocida.')
    antecedentes_quirurgicos = fields.Text(string='Antecedentes Quirúrgicos')
    sexualmente_activo = fields.Boolean(string='Sexualmente Activo')
    metodo_planificacion = fields.Selection([
        ('pildora', 'Píldora'),
        ('inyeccion', 'Inyección'),
        ('t_cobre', 'T-Cobre'),
        ('ritmo', 'Ritmo'),
        ('condon', 'Condón'),
        ('ninguno', 'Ninguno')
    ], string='Método de Planificación', default='ninguno')
    numero_embarazos = fields.Integer(string='Número de Embarazos', required=False)
    numero_partos = fields.Integer(string='Número de Partos', required=False)
    numero_abortos = fields.Integer(string='Número de Abortos', required=False)
    numero_cesareas = fields.Integer(string='Número de Cesáreas', required=False)
    fecha_ultima_citologia = fields.Date(string='Fecha de Última Citología')
    show_ginecologicos = fields.Boolean(string="Mostrar Pestaña Ginecológicos", compute="_compute_show_ginecologicos")
    consultation_count = fields.Integer(string='Consultas', compute='_compute_consultation_count', store=False)
    appointment_count = fields.Integer(string='Citas', compute='_compute_appointment_count', store=False)
    total_invoiced = fields.Monetary(string='Monto Facturado', compute='_compute_total_invoiced', currency_field='currency_id', store=False)
    currency_id = fields.Many2one('res.currency', string='Moneda', default=lambda self: self.env.company.currency_id, required=True)
    
    #Con esto agregamos el campo de compañía
    company_id = fields.Many2one(
    'res.company',
    string='Compañía',
    default=lambda self: self.env.company,
    required=True
    )


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
                vals['sequence'] = self.env['ir.sequence'].next_by_code('clinica.paciente') or _("New")
        return super(HospitalPatient, self).create(vals_list)

    @api.depends('gender')
    def _compute_show_ginecologicos(self):
        for record in self:
            record.show_ginecologicos = record.gender == 'female'



    def _compute_total_invoiced(self):
        for record in self:
            invoices = self.env['account.move'].search([
                ('partner_id', '=', record.contact_id.id),
                ('state', '=', 'posted'),
                ('move_type', '=', 'out_invoice')
            ])
            record.total_invoiced = sum(invoices.mapped('amount_total'))

    def action_view_invoices(self):
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
