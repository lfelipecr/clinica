from odoo import http
from odoo.http import request

class CitasController(http.Controller):

    @http.route('/solicitarcita', type='http', auth='public', website=True)
    def cita_form(self, **kw):
        especialidades = request.env['clinica.especialidad'].sudo().search([])
        return request.render('hospital.cita_form_template', {
            'especialidades': especialidades,
        })

    @http.route('/crearcita', type='http', auth='public', website=True, methods=['POST'])
    def crear_cita(self, **post):
        paciente = request.env['res.partner'].sudo().search([('email', '=', post.get('email'))], limit=1)
        if not paciente:
            paciente = request.env['res.partner'].sudo().create({
                'name': post.get('nombre'),
                'email': post.get('email'),
                'phone': post.get('telefono'),
            })

        request.env['clinica.cita'].sudo().create({
            'paciente_id': paciente.id,
            'especialidad_id': int(post.get('especialidad')),
            'medico_id': int(post.get('medico')),
            'fecha_cita': post.get('fecha_hora'),
            'comentarios': post.get('comentarios'),
        })

        return request.render('hospital.cita_confirmacion_template', {})

    @http.route('/hospital/obtenermedicos', type='json', auth='public')
    def obtener_medicos(self, especialidad_id):
        especialidad = request.env['clinica.especialidad'].sudo().browse(int(especialidad_id))
        medicos = especialidad.medico_ids
        return [{'id': medico.id, 'name': medico.name.name} for medico in medicos]
