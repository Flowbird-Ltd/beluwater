# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

{
    'name': "Partner Org Chart ",
    'version': '13.0.1.0',
    'category': 'Tools',
    'author': 'Equick ERP',
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
        'views/template.xml',
        'views/res_partner_view.xml'
    ],
    'images': ['static/description/main_screenshot.png'],
    'qweb': [
        'static/src/xml/partner_chart.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: