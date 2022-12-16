#!/usr/bin/python3
"""module is document"""
from api.v1.views import app_views
from flask import jsonify, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], defaults={"state_id":None}, strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_get(state_id):
    """documentation"""

    list_obj = []
    if state_id and storage.get(State, state_id) is None:
        return make_response(jsonify({"error": "Not found"}), 404)

    if state_id:
        return jsonify((storage.get(State, state_id).to_dict()))
    else:
        for i in storage.all(State).values():
            list_obj.append(i.to_dict())
    return jsonify(list_obj)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def states_delete(state_id):
    """documentation full"""
    if storage.get(State, state_id) is None:
        return make_response(jsonify({"error": "Not found"}), 404)
    obj = storage.get(State, state_id)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>', methods=['POST'], strict_slashes=False)
def states_post():
    """documentation"""
    obj = request.get_json(silent=True, force=True)
    if obj is None:
        make_response(jsonify({"error": "Not found"}), 404)
    if  not obj["name"]:
        make_response(jsonify({"error": "Not found"}), 404)
    newState = State()
    for key, value in obj.items():
        setattr(newState, key, value)
    storage.new(newState)
    storage.save()
    return make_response(jsonify(newState.to_dict()), 200)

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def states_put(state_id):
    """documented"""
    json_obj = request.get_json(silent=True, force = True)
    if json_obj is None:
        make_response(jsonify({"error": "Not found"}), 404)
    if  not json_obj["name"]:
        make_response(jsonify({"error": "Not found"}), 404)
    obj = storage.get(State, state_id)
    if obj is None:
        return make_response(jsonify({"error":"Not found"}), 404)
    for key, value in json_obj.items():
         setattr(obj, key, value)
    obj.save()
    return make_response(jsonify(obj.to_dict(), 200))