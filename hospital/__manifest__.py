{
    'name': "Hospital",
    'author': "Kibudoo",
    'website': "https://www.Kibudoo.com/",
    'summary': """Modulo para clinicas""",
    'version': '2017.11.1',
    'depends': ['mail', 'portal', 'base', 'contacts', 'product', 'account'],
    'data': [
        'security/hospital_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/ir_sequence_data.xml',
        'views/hospital_patient_view.xml',
        'views/hospital_doctor_view.xml',
        'views/hospital_appointment_view.xml',
        'views/hospital_consultation_views.xml',
        'views/hospital_consultation_type_views.xml',  # Cambiado: Ahora antes de hospital_menu.xml
        'views/hospital_exam_type_views.xml',  # Nuevo archivo de vistas
        'views/hospital_exam_views.xml',  # Nuevo archivo para exámenes
        'views/hospital_menu.xml',  # Menú cargado al final para evitar referencias inválidas
    ],
    'installable': True,
    'application': True,
    'auto_installable': False,
    'license': 'LGPL-3',
}
