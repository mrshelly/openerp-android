# -*- coding: utf-8 -*-

from osv import fields, osv
from tools.translate import _

class res_sms_message(osv.osv):
    _name = "res.sms.message"
    _description = "SMS Message"
    _rec_name = 'address'

    _columns = {
        'simcard_id': fields.many2one('sim.card', 'Sim Card'),
        'folder': fields.selection([
            ('inbox', 'In Box'),
            ('outbox', 'Out Box'),
            ('draft', 'Draft Box'),
            ], 'Folder', help="SMS Message Folder."),
        'sim_id': fields.char('Sim Card ID', help="The SIM Card sequence."),
        'protocol': fields.integer('SMS Protocol'),
        'type': fields.integer('Type'),
        'service_center': fields.char('Service Center', size=20),
        'address': fields.char('Sender Number', size=20),
        'locked': fields.integer('Locked'),
        'reply_path_present': fields.integer('Reply Path Present'),
        'read': fields.integer('Readed'),
        'person': fields.integer('Person'),
        'thread_id': fields.integer('Thread ID'),
        'date': fields.char('Date', size=20),
        'date_sent': fields.char('Date Sent', size=20),
        'seen': fields.integer('Seen'),
        'body': fields.char('Body', size=300),
        'm_size': fields.integer('Max Size'),
        'o_id': fields.integer('Source ID'),
        'error_code': fields.char('Error Code', size=10),
        'status': fields.char('Status', size=20),
    }

    _defaults = {
        'folder': 'inbox',
    }

res_sms_message()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
