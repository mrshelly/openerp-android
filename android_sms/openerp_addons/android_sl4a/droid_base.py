# -*- coding: utf-8 -*-

import socket,time
socket.setdefaulttimeout(3)

from osv import fields, osv
from tools.translate import _
from sl4a import android

socket_trytimes = [0.1, 2]

class droid_devices(osv.osv):
    _name = "droid.device"
    _description = "Android Devices"
    _droid = {}

    _columns = {
        'name': fields.char('Name', size=64, required=True, help="The device's name."),
        'code': fields.char('Code', size=3, required=True, help="The device's rule code."),
        'host': fields.char('Host', size=64, help="The sl4a's listen interface."),
        'port': fields.integer('Port', help="The sl4a's listen port."),
        'simcard_ids': fields.one2many('sim.card', 'device_id', 'Sim Cards'),
        'last_connect_ts': fields.integer('Last Connect Timestamp'),
        'last_offline_ts': fields.integer('Last OffLine Timestamp'),
        'state': fields.selection([
            ('online', 'On-Line'),
            ('offline', 'Off-Line'),
            ('except', 'Exception'),
            ], 'State', readonly=True, help="The device's current state."),
        'active': fields.boolean('Active'),
    }
    _defaults = {
        'host': '127.0.0.1',
        'port': 10000,
        'active': True,
        'state': 'offline',
    }

    def _init_instance(self, cr, uid, ids, context=None):
        '''
            Init the device connect pool.
        '''
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = self.browse(cr, uid, ids, context=context)
        ret = False
        for r in res:
            try:
                if r.active:
                    self._droid[str(r.id)] = android.Android((r.host, int(r.port)))
                    ret = True
            except:
                pass
        return ret

    def test_connect(self, cr, uid, ids, context=None):
        '''
            To check the connect status.
        '''
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = self.browse(cr, uid, ids, context=context)
        ret = {}
        for r in res:
            ret[str(r.id)] = False
            for ts in socket_trytimes:
                try:
                    if r.active:
                        ret[str(r.id)] = self._droid[str(r.id)].wifiGetConnectionInfo()
                        self.write(cr, uid, r.id, {'state':'online'}, context=context)
                except KeyError, ex:
                    if not self._init_instance(cr, uid, r.id, context=context):
                        self.write(cr, uid, r.id, {'last_offline_ts':time.time(), 'state':'offline'}, context=context)
                    continue
                except AttributeError, ex:
                    if not self._init_instance(cr, uid, r.id, context=context):
                        self.write(cr, uid, r.id, {'last_offline_ts':time.time(), 'state':'offline'}, context=context)
                    continue
                except socket.error, ex:
                    if not self._init_instance(cr, uid, r.id, context=context):
                        self.write(cr, uid, r.id, {'last_offline_ts':time.time(), 'state':'offline'}, context=context)
                    continue
                except:
                    self.write(cr, uid, r.id, {'last_offline_ts':time.time(), 'state':'except'}, context=context)
                finally:
                    time.sleep(ts)
                break
        return ret

    def act_refresh(self, cr, uid, ids, context=None):
        '''
            To check the connect status. and update the status of android device.
        '''
        if context is None:
            context = {}
        self.test_connect(cr, uid, ids, context=context)
        return {'type':'ir.actions.act_window_close' }

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
        'sms_message_ids': fields.one2many('res.sms.message', 'simcard_id', 'SMS Messages'),
        'state': fields.related('device_id', 'state', type="selection", selection=[
            ('online', 'On-Line'),
            ('offline', 'Off-Line'),
            ('except', 'Exception'),
            ], string="State", readonly=True),
        'active': fields.related('device_id', 'active', type="boolean", string="Active", readonly=True),
    }

    _defaults = {
        'isp': 'china_mobile',
    }

    _sql_constraints = [
        ('code', 'unique (code)', 'The code of the sim card must be unique !')
    ]

    def get_allsms(self, cr, uid, ids, context=None):
        '''
            Get all sms message of the android device.
        '''
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        device_obj = self.pool.get('droid.device')
        sms_msg_obj = self.pool.get('res.sms.message')
        res = self.browse(cr, uid, ids, context=context)
        ret = []
        for r in res:
            if r.device_id.sms_simcard_id.id != r.id:
                continue
            device_obj.test_connect(cr, uid, r.device_id.id, context=context)
            if r.active:
                attrs = device_obj._droid[str(r.device_id.id)].smsGetAttributes().result
                time.sleep(0.01)
                msg_res = device_obj._droid[str(r.device_id.id)].smsGetMessages(False, 'inbox', attrs).result
                if isinstance(msg_res, list) and len(msg_res)>0:
                    for rr in msg_res:
                        o_ids = sms_msg_obj.search(cr, uid, [('o_id', '=', int(rr['_id']))], context=context)
                        if len(o_ids)>0:
                            continue
                        tmp_res = {
                            'body': rr['body'],
                            'status': rr['status'],
                            'protocol': int(rr['protocol']),
                            'sim_id': rr['sim_id'],
                            'read': int(rr['read']),
                            'type': int(rr['type']),
                            'service_center': rr['service_center'],
                            'address': rr['address'],
                            'locked': int(rr['locked']),
                            'reply_path_present': int(rr['reply_path_present']),
                            'person': int(rr['person']),
                            'thread_id': int(rr['thread_id']),
                            'date': long(rr['date']),
                            'date_sent': long(rr['date_sent']),
                            'seen': int(rr['seen']),
                            'o_id': int(rr['_id']),
                            'error_code': rr['error_code'],
                        }

                        tmp_res.update({'folder': 'inbox'})
                        ret.append(sms_msg_obj.create(cr, uid, tmp_res, context=context))
        return ret

    def act_get_allsms(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        sms_ids = self.get_allsms(cr, uid, ids, context=context)
        ret ={
            'name': _('SMS Messages'),
            'type': 'ir.actions.act_window',
            'domain': [('folder', '=', 'inbox')],
            'context': context,
            'res_model': 'res.sms.message',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'iframe',
            'auto_refresh': 20,
        }
        return ret

sim_card()

class droid_devices_inherit_sms_card(osv.osv):
    _name = "droid.device"
    _inherit = "droid.device"

    _columns = {
        'sms_simcard_id': fields.many2one('sim.card', 'SMS SimCard'),
    }

    def _getMessageCnt(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = self.read(cr, uid, ids, context=context)
        self.test_connect(cr, uid, ids, context=context)
        for r, in res:
            ret[str(r.id)] = 0
            if r.state in ['offline', 'except']:
                continue
            try:
                if r.active:
                    ret[str(r.id)] = self._droid[str(r.id)].smsGetMessageCount(False)
            except socket.error, ex:
                if r.active and r.state in ['online']:
                    self.write(cr, uid, r.id, {'last_offline_ts':time.time(), 'state':'offline'}, context=context)
            except:
                pass
        return ret

droid_devices_inherit_sms_card()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
