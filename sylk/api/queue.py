import logging

from flask import Blueprint
from flask_cors import CORS
from flask_restful import reqparse

from ..db.queue import add_calltaker_to_queue, add_queue, get_queue_details, get_queue_members, \
    remove_calltaker_from_queue, remove_queue, edit_queue, get_queues
from .decorators import check_exceptions
from .utils import get_argument

queue = Blueprint('queue', __name__,
                        template_folder='templates')

CORS(queue)

log = logging.getLogger('emergent-ng911')


@queue.route('/all/<psap_id>', methods=['GET'])
@check_exceptions
def all(psap_id):
    return {
        "queues" : get_queues(psap_id)
    }


@queue.route('/add', methods=['POST', 'PUT'])
@check_exceptions
def api_add_queue():
    queue_name = get_argument('queue_name')
    psap_id = get_argument('psap_id')
    user_ids = get_argument('user_ids')
    return add_queue(psap_id, queue_name, user_ids)


@queue.route('/delete/<queue_id>', methods=['POST', 'PUT'])
@check_exceptions
def api_delete_queue(queue_id):
    remove_queue(queue_id)


@queue.route('/<queue_id>', methods=['POST', 'PUT'])
@check_exceptions
def api_edit_queue(queue_id):
    queue_name = get_argument('queue_name')
    user_ids = get_argument('user_ids')
    edit_queue(queue_id, queue_name, user_ids)


@queue.route('/<queue_id>', methods=['GET'])
@check_exceptions
def api_queue_details(queue_id):
    return get_queue_details(queue_id)


@queue.route('/users/<queue_id>', methods=['GET'])
@check_exceptions
def api_queue_calltakers(queue_id):
    return {
        "users" : get_queue_members(queue_id)
    }


@queue.route('/user/add', methods=['POST', 'PUT'])
@check_exceptions
def api_add_calltaker_to_queue():
    parser = reqparse.RequestParser()
    parser.add_argument('queue_id', required=True)
    parser.add_argument('user_id', required=True)
    payload = parser.parse_args()
    add_calltaker_to_queue(payload["user_id"], payload["queue_id"])


@queue.route('/user/delete', methods=['POST', 'PUT'])
@check_exceptions
def api_delete_calltaker_from_queue():
    parser = reqparse.RequestParser()
    parser.add_argument('queue_id', required=True)
    parser.add_argument('user_id', required=True)
    payload = parser.parse_args()
    user_id = payload["user_id"]
    queue_id = payload["queue_id"]
    log.info("removing userid %s from queue %s", user_id, queue_id)
    remove_calltaker_from_queue(user_id, queue_id)
