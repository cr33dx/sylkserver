from autobahn.twisted.component import Component
from sylk.applications import ApplicationLogger
from application.notification import IObserver, NotificationCenter, NotificationData
from sylk.utils import dump_object_member_vars, dump_object_member_funcs
log = ApplicationLogger(__package__)
from twisted.internet.defer import inlineCallbacks, returnValue
from sylk.data.calltaker import CalltakerData

log.info("wamp session start")

comp = Component(
     transports=u"ws://159.65.73.31:8080/ws",
     realm=u"realm1",
     extra="tarun"
 )

wamp_session=None

def publish_update_calltaker_status(user_id, username, status):
    if wamp_session is not None:
        json_data = {
            'username': username,
            'user_id': user_id,
            'status': status
        }
        wamp_session.publish(u'com.emergent.calltaker', json_data)

def publish_update_calltakers(json_data):
    if wamp_session is not None:
        wamp_session.publish(u'com.emergent.calltakers', json_data)

def publish_create_call(call_data):
    if wamp_session is not None:
        json_data = {}
        json_data['command'] = 'created'
        json_data['room_number'] = call_data['room_number']
        json_data['call_data'] = call_data
        log.info("publish com.emergent.call with json %r", json_data)
        wamp_session.publish(u'com.emergent.call', json_data)

def publish_active_call(calltaker, room_number):
    if wamp_session is not None:
        json_data = {}
        json_data['command'] = 'active'
        json_data['room_number'] = room_number
        wamp_session.publish(u'com.emergent.call.%s' % calltaker, json_data)
    pass

def publish_update_call(room_number, call_data):
    if wamp_session is not None:
        json_data = {}
        json_data['command'] = 'updated'
        json_data['room_number'] = room_number
        json_data['call_data'] = call_data
        log.info("publish com.emergent.call with json %r", json_data)
        wamp_session.publish(u'com.emergent.call', json_data)

def publish_update_calls():
    if wamp_session is not None:
        log.info("publish com.emergent.calls")
        wamp_session.publish(u'com.emergent.calls')

@comp.on_join
@inlineCallbacks
def joined(session, details):
    global wamp_session
    log.info("wamp session ready %r, id %r", session, session._session_id)
    # make sure calltaker is initialized
    CalltakerData()
    wamp_session = session

    def on_calltaker_status(data):
        log.info("event on_calltaker_status received")
        log.info("event on_calltaker_status received: %r", data)
        log.info("event on_calltaker_status received: %r", data['command'])
        if data['command'] == 'status':
            log.info("process status command")
            notification_center = NotificationCenter()
            notification_data = NotificationData(username=data['username'], \
                                                  status=data['status'], wamp_session_id=data['wamp_session_id'], user_id=data['user_id'])
            notification_center.post_notification('CalltakerStatus', session, notification_data)
            out = {
                'command' : 'status_updated'
            }
            session.publish(u'com.emergent.calltakers', out)
            log.info("sent status_updated")

    def on_session_leave(data):
        log.info("on_session_leave event received")
        log.info("on_session_leave event received: %r", data)
        notification_center = NotificationCenter()
        notification_center.post_notification('CalltakerSessionLeave', session, NotificationData(wamp_session_id=data))
        out = {
            'command': 'status_updated'
        }
        session.publish(u'com.emergent.calltakers', out)

    try:
        yield session.subscribe(on_session_leave, u'wamp.session.on_leave')
        log.info("subscribed to wamp.session.on_leave")

        res = yield session.subscribe(on_calltaker_status, u'com.emergent.calltakers')
        log.info("subscribed to topic %r, id %r", res, res.id)
        data = {
            'command' : 'send_status_update'
        }

        yield session.publish(u'com.emergent.calltakers', data)
        '''
        out = {
            'command': 'status_updated'
        }
        yield session.publish(u'com.emergent.calltakers', out)
        '''

    except Exception as e:
        log.info("exception in subscribe to topic: %r" % e)
    '''
    dump_object_member_vars(log, session)
    dump_object_member_funcs(log, session)
    log.info("wamp session id %r" % session._session_id)
    log.info("wamp confog %r" % session.config)
    dump_object_member_vars(log, session.config)
    dump_object_member_funcs(log, session.config)
    log.info("wamp config extra %r" % session.config.extra)
    '''

@comp.on_leave
@inlineCallbacks
def left(session, details):
    global wamp_session
    log.info("session left")
    wamp_session = None
    # todo - try to reconnect here


def start():
     comp.start()
