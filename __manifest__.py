# -*- coding: utf-8 -*-
{
    'name': "Curso rNet",

    'summary': """
        Adminitscion de cursos""",

    'description': """
        Modulo de rNet para Administrar cursos:
        Gestion de cursos
        Gestion de Sesiones
        Registro de participantes
    """,

    'author': "Rafael Espinoza",
    'website': "http://www.rnet.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'demo/demo.xml',
        'views/curso_rnet.xml',
        'views/partner.xml',
        'views/wizard.xml',
        'report/reporte_sesion.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
