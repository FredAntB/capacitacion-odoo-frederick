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
    'category': 'Hostel',
    'version': '17.0.1.0.0',
    'depends': ['base', 'mail', 'web'],
    'data': [ "security/hostel_security.xml",
             "security/groups.xml",
             "views/assign_room_student_wizard.xml",
             "views/hostel.xml",
             "security/ir.model.access.csv",
             "security/groups.xml",
             "views/hostel_room.xml",
             "views/hostel_student.xml",
             "views/hostel_amenities.xml",
             "views/hostel_room_stages_views.xml",
             "views/hostel_categ.xml",
             "views/templates.xml",
             "data/data.xml",
             "data/room_stages.xml"],
    'assets': {
        'web.assets_backend': [
            'my_hostel/static/src/scss/field_widget.scss',
            'my_hostel/static/src/js/field_widget.js',
            "my_hostel/static/src/js/component.js",
            'my_hostel/static/src/xml/field_widget.xml'
        ],
    },
    'demo': ['demo.xml'],
    'installable': True, # Good practice to explicitly state this
    'application': True, # If it's a primary app, set to True
    'license': 'LGPL-3', # Recommend adding a license
}
