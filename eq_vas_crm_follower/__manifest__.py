# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################
{
    'name': "CRM Follower",
    'category': 'CRM',
    'version': '13.0.1.0',
    'author': 'Equick ERP',
    'description': """
        CRM Follower
        * Ref No: S00054
    """,
    'summary': """CRM Follower.""",
    'depends': ['mail', 'crm'],
    'license': 'OPL-1',
    'website': "",
    'data': [
        'views/crm_view.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: