from odoo import http
from odoo.http import request
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class CitaController(http.Controller):

    @http.route('/solicitar_cita', type='http', auth='public', website=True)
    def solicitar_cita_form(self, **kwargs):
        """Renderiza el formulario público para solicitar una cita."""
        medicos = request.env['clinica.medico'].sudo().search([])
        return request.render('hospital.cita_form_new', {'medicos': medicos})

    @http.route('/enviar_cita', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def enviar_cita(self, **post):
        """Procesa los datos enviados desde el formulario."""
        # Capturar el token CSRF desde el formulario
        csrf_token = post.get('csrf_token')
        session_id = request.httprequest.cookies.get('session_id')
        _logger.info(f"CSRF token recibido: {csrf_token}")
        _logger.info(f"CSRF token esperado: {request.csrf_token()}")
        _logger.info(f"Session ID de la cookie: {session_id}")
        _logger.info(f"Session context: {request.session}")
        _logger.info(f"CSRF token generado: {request.csrf_token()}")


        # Validar el token CSRF
        if not csrf_token or csrf_token != request.csrf_token():
            _logger.warning("CSRF token no válido o ausente.")
            return request.render('hospital.cita_form_new', {
                'error': '<div style="color: red;">Token CSRF inválido. Por favor, intente nuevamente.</div>',
                'medicos': request.env['clinica.medico'].sudo().search([])
            })

        # Datos del formulario
        nombre = post.get('nombre')
        correo = post.get('correo')
        telefono = post.get('telefono')
        fecha_cita = post.get('fecha_cita')
        medico_id = int(post.get('medico_id'))
        observaciones = post.get('observaciones')

        # Validaciones básicas
        if not nombre or not correo or not telefono or not fecha_cita or not medico_id:
            return request.render('hospital.cita_form_new', {
                'error': 'Todos los campos son obligatorios',
                'medicos': request.env['clinica.medico'].sudo().search([])
            })

        # Verificar si existe un paciente con el correo o teléfono
        paciente = request.env['clinica.paciente'].sudo().search(
            ['|', ('email', '=', correo), ('telefono', '=', telefono)], limit=1
        )

        # Si no existe, creamos un nuevo paciente
        if not paciente:
            paciente = request.env['clinica.paciente'].sudo().create({
                'name': nombre,
                'email': correo,
                'telefono': telefono
            })

        # Crear la cita
        request.env['clinica.cita'].sudo().create({
            'paciente_id': paciente.id,
            'medico_id': medico_id,
            'fecha_cita': datetime.strptime(fecha_cita, '%Y-%m-%d %H:%M:%S'),
            'notes': observaciones,
            'estado': 'draft'
        })

        # Mensaje de éxito
        return request.render('hospital.cita_success', {})
