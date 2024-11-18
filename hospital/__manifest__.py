{
    'name': "Hospital",
    'author': "Kibudoo",
    'website': "https://www.Kibudoo.com/",
    'summary': """Modulo para clinicas""",
    'version': '2017.11.1',
    'depends': ['mail', 'portal', 'base', 'contacts','product'],
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