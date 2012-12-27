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
        'simcard_ids': fields.one2many('sim.card', 'device_id', 'Sim Cards'),
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

class sim_card(osv.osv):
    _name = "sim.card"
    _description = "SIM Card"

    _columns = {
        'device_id': fields.many2one('droid.device', 'On Device', required=True, ondelete="cascade"),
        'code': fields.char('Code', size=64, required=True, help="SIM Card No."),
        'name': fields.char('Name', size=64, required=True, help="SIM Card Name."),
        'isp': fields.selection([
            ('china_mobile', 'China Mobile'),
            ('china_unicom', 'China Unicom'),
            ('china_telecom', 'China Telecom'),
            ],'ISP'),
        'state': fields.selection([
            ('online', 'On-Line'),
            ('offline', 'Off-Line'),
            ('except', 'Exception'),
            ], 'State'),
        'active': fields.boolean('Active'),
    }

    _sql_constraints = [
        ('code', 'unique (code)', 'The code of the sim card must be unique !')
    ]

sim_card()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
