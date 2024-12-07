{
    'name': "Hospital",
    'author': "Kibu INC",
    'website': "https://www.Kibuinc.com/",
    'summary': """Modulo para clinicas""",
    'version': '2017.11.1',
    'depends': ['mail', 'portal', 'base', 'contacts', 'product', 'account', 'hr', 'website'],
    'data': [
        # Seguridad y acceso
        'security/clinica_security.xml',
        'security/ir.model.access.csv',
        # Secuencias
        'data/sequence.xml',  # Incluye el archivo de secuencias
        # Vistas
        'views/paciente_views.xml',
        'views/medico_views.xml',
        'views/especialidad_views.xml',
        'views/citas.xml',  # Agrega el archivo de vistas de citas
        'views/examen_views.xml', 
        'views/consulta_views.xml',
        'views/product_template_views.xml',
        'views/receta_views.xml',  # Vistas para recetas
        'views/menus.xml',
        # Plantillas del sitio web
        'views/cita_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'hospital/static/src/js/cita_form.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,  # Corregido el nombre de la clave
    'license': 'LGPL-3',
}
