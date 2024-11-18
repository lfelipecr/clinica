from odoo import models, fields, api, _
from datetime import date  # Importar `date` del módulo `datetime`

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Patients'

    # Elimina el campo `name`
    # name = fields.Char(string='Nombre', required=True, tracking=True)   

    sequence = fields.Char(string='Sequence', default="New", readonly=True)
    contact_id = fields.Many2one(comodel_name='res.partner',string='Contacto',ondelete='set null',help='Selecciona el contacto asociado a este paciente.')
    phone = fields.Char(related='contact_id.phone', string='Teléfono', readonly=True)
    email = fields.Char(related='contact_id.email', string='Correo Electrónico', readonly=True)
    nacimiento = fields.Date(string='Fecha de Nacimiento', required=False, tracking=True)  # Campo de fecha de nacimiento agregado
    age = fields.Integer(string='Edad', compute='_compute_age', store=False, tracking=True) #Calcula la edad automaticamente
    gender = fields.Selection(string='Genero', selection=[('male', 'Masculino'), ('female', 'Femenino')], default='male', tracking=True)
    # email = fields.Char(string='Correo')
    company_id = fields.Many2one(comodel_name='res.company', default=lambda self: self.env.company)
    peso = fields.Integer(string='Peso (kg)', required=False, tracking=True)
    altura = fields.Integer(string='Altura (cm)', required=False, tracking=True)
    imc = fields.Float(string='IMC', compute='_compute_imc', store=True, readonly=True)
    antecedentes_personales = fields.Text(string='Antecedentes Personales')
    medicamentos_actuales = fields.Many2many(comodel_name='product.product', string='Medicamentos Actuales')
    fuma = fields.Boolean(string='Fuma')
    alcohol = fields.Boolean(string='Consumo de Alcohol')
    drogas = fields.Boolean(string='Uso de Drogas')
    cocina_lena = fields.Boolean(string='¿Usa cocina de leña?')
    antecedentes_heredofamiliares = fields.Text(string='Antecedentes Heredofamiliares')
    antecedentes_quirurgicos = fields.Text(string='Antecedentes Quirúrgicos')
    vacunas = fields.Selection(
    string='Vacunas',
    selection=[
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
    ],
    help='Vacuna aplicada al paciente según el esquema de vacunación de Costa Rica.'
    )

    sexualmente_activo = fields.Boolean(string='Sexualmente Activo')
    metodo_planificacion = fields.Selection(string='Método de Planificación',
                                            selection=[('pildora', 'Píldora'),
                                                       ('inyeccion', 'Inyección'),
                                                       ('t_cobre', 'T-Cobre'),
                                                       ('ritmo', 'Ritmo'),
                                                       ('condon', 'Condón'),
                                                       ('ninguno', 'Ninguno')], default='ninguno')
    numero_embarazos = fields.Integer(string='Número de Embarazos', required=False)
    numero_partos = fields.Integer(string='Número de Partos', required=False)
    numero_abortos = fields.Integer(string='Número de Abortos', required=False)
    numero_cesareas = fields.Integer(string='Número de Cesáreas', required=False)
    fecha_ultima_citologia = fields.Date(string='Fecha de Última Citología')



    @api.depends('nacimiento')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.nacimiento:
                nacimiento = fields.Date.from_string(record.nacimiento)
                record.age = today.year - nacimiento.year - ((today.month, today.day) < (nacimiento.month, nacimiento.day))
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
