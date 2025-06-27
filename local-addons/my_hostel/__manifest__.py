{
    'name': "Hostel Management",
    'summary': "Manage Hostel easily",
    'description': """
        Efficiently manage the entire residential facility in the school.
    """, # Use triple quotes for multi-line strings.
    # Note: 'description' key is not deprecated, but its content is often simplified
    # and longer descriptions are put in a README.md or similar.
    'author': "Your name",
    'website': "http://www.example.com",
    'category': 'Uncategorized',
    'version': '17.0.1.0.0',
    'depends': ['base'],
    'data': [ "security/hostel_security.xml",
             "views/assign_room_student_wizard.xml",
             "security/ir.model.access.csv",
             "views/hostel.xml",
             "views/hostel_room.xml",
             "views/hostel_categ.xml",
             "views/hostel_student.xml",
             "data/data.xml"],
    'assets': {
        'web.assets_backend': [
            'web/static/src/xml/**/*',
        ],
    },
    'demo': ['demo.xml'],
    'installable': True, # Good practice to explicitly state this
    'application': True, # If it's a primary app, set to True
    'license': 'LGPL-3', # Recommend adding a license
}
