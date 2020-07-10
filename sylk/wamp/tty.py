import traceback
import time
try:
    from sylk.applications import ApplicationLogger
    log = ApplicationLogger(__package__)
except:
    import logging
    log = logging.getLogger('emergent-ng911')

from .core import wamp_publish


def publish_tty_enabled(room_number):
    try:
        json_data = {}
        json_data['room_number'] = room_number
        wamp_publish(u'com.emergent.call.tty.enabled', json_data)
    except Exception as e:
        stackTrace = traceback.format_exc()
        log.error("exception in publish_tty_enabled %s", str(e))
        log.error("%s", stackTrace)

def publish_tty_updated(room_number):
    try:
        json_data = {}
        json_data['room_number'] = room_number
        wamp_publish(u'com.emergent.call.tty.updated', json_data)
    except Exception as e:
        stackTrace = traceback.format_exc()
        log.error("exception in publish_tty_updated %s", str(e))
        log.error("%s", stackTrace)

