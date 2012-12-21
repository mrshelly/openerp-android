# -*- coding: utf-8 -*-

from osv import fields, osv
from tools.translate import _

class droid_devices(osv.osv):
    _name = "droid.device"
    _description = "Android Devices"
    _columns = {
        'name': fields.char('Name', size=64, required=True, help="The device's name."),
        'code': fields.char('Code', size=3, required=True, help="The device's rule code."),
        'host': fields.char('Host', size=64, help="The sl4a's listen interface."),
        'port': fields.integer('Port', help="The sl4a's listen port."),
        'state': fields.selection([
            ('online', 'On-Line'),
            ('offline', 'Off-Line'),
            ('except', 'Exception'),
            ], 'State', help="The device's current state."),
        'active': fields.boolean('Active'),
    }
    _defaults = {
        'host': '127.0.0.1',
        'port': 10000,
        'active': True,
        'state': 'offline',
    }

droid_devices()
