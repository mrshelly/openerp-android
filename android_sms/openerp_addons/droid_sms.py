# -*- coding: utf-8 -*-

from osv import fields, osv
from tools.translate import _

class res_sms_message(osv.osv):
    _name = "res.sms.message"
    _description = "SMS Message"
    _rec_name = 'address'

    _columns = {
        'sim_id': fields.integer('Sim Card ID', help="The SIM Card sequence."),
        'protocol': fields.integer('SMS Protocol'),
        'type': fields.integer('Type'),
        'service_center': fields.char('Service Center', size=20),
        'address': fields.char('Sender Number', size=20),
        'reply_path_present': fields.integer('Reply Path Present'),
        'read': fields.integer('Readed'),
        'person': fields.integer('Person'),
        'thread_id': fields.integer('Thread ID'),
        'date': fields.integer('Date'),
        'date_sent': fields.integer('Date Sent'),
        'seen': fields.integer('Seen'),
        'body': fields.char('Body', size=300),
        'm_size': fields.integer('Max Size'),
        'o_id': fields.integer('Source ID'),
        'error_code': fields.char('Error Code'),
        'status': fields.char('Status'),
    }

res_sms_message()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
