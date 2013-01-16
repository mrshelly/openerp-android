# -*- encoding: utf-8 -*-

{
    'name': 'OpenERP Android SL4A SMS',
    'version': '0.2',
    'category': 'Generic Modules/Messages',
    'description': """
        To communicate android device by SL4A(Script Layer for Android)
    """,
    'author': 'mrshelly',
    'website': 'https://github.com/mrshelly/openerp-android',
    'depends': ['base'],
    'init_xml': [
    ],
    'update_xml': [
        'security/android_security.xml',
        'security/ir.model.access.csv',
        'view/android_device_view.xml',
        'view/message_view.xml',
    ],
    'demo_xml': [],
    'installable': True,
    'active': False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
