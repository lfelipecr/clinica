{
    'name': "Hospital",
    'author': "Escuela Full Stack",
    'website': "https://escuelafullstack.com/",
    'summary': """Modulo para hospitales""",
    'depends': ['mail', 'portal'],
    'data': [
        'security/hospital_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/hospital_patient_view.xml',
        'views/hospital_doctor_view.xml',
        'views/hospital_appointment_view.xml',
        'views/hospital_menu.xml'
    ],
    'installable': True,
    'application': True,
    'auto_installable': False,
    'license': 'LGPL-3'
}