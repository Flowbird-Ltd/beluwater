# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

{
    'name': "Partner Org Chart",
    'version': '15.0.1.0',
    'category': 'Tools ',
    'author': '',
    'summary': """Organization Chart for Contact""" ,
    'description': """
        Org Chart Widget for Partner/Contact
        =======================
        * This module extend the Contact form with a organizational chart.
        * User can see Parent and Child contact of current contact.
    """,
    'license': 'OPL-1',
    'depends': ['base'],
    'price': 30,
    'currency': 'EUR',
    'website': "",
    'data': [
        # 'views/template.xml',
        'views/res_partner_view.xml'
    ],
    'images': ['static/description/main_screenshot.png'],
    'assets': {
        'web._assets_primary_variables': [
            'eq_partner_org_chart/static/src/scss/variables.scss',
        ],
        'web.assets_backend': [
            'eq_partner_org_chart/static/src/scss/org_chart.scss',
            'eq_partner_org_chart/static/src/js/partner_chart.js',
        ],
        'web.assets_qweb': [
            'eq_partner_org_chart/static/src/xml/partner_chart.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
