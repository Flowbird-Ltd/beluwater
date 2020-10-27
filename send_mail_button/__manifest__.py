# -*- encoding: utf-8 -*-
{
    'name' : 'test sen button',
    'version': '0.1',
    'summary': 'Module customization',
    'category': 'Custom Development',
    'author': 'Odoo Inc',
    'description':
        """
Test
==============

send email button
        """,
    'data': ['views/crm_lead_view.xml', 'views/res_partner_view.xml'],
    'depends': ['crm', 'contacts'],
}
