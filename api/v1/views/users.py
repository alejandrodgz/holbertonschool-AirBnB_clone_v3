#!/usr/bin/python3
"""this module is documented right here"""

from api.v1.views import app_views
from flask import jsonify, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def allUser():
    """documentation of this method"""

    return jsonify([user.to_dict() for user in storage.all(User).values()])


@app_views.route('users/<user_id>', methods=['GET'], strict_slashes=False)
def UserById(user_id):
    """documentation of this method"""

    if not storage.get(User, user_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    return jsonify(storage.get(User, user_id).to_dict())


@app_views.route('users/<user_id>', methods=['DELETE'], strict_slashes=False)
def UserDelete(user_id):
    """documentation of this method"""

    if not storage.get(User, user_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    storage.delete(storage.get(User, user_id))
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def userPost():
    """documentation of this method"""

    dataObj = request.get_json()
    if not dataObj:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in dataObj:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in dataObj:
        return make_response(jsonify({"error": "Missing password"}), 400)
    newUser = User()
    for key, value in dataObj.items():
        setattr(newUser, key, value)
    storage.new(newUser)
    storage.save()
    return make_response(jsonify(newUser.to_dict()), 201)


@app_views.route('users/<user_id>', methods=['PUT'], strict_slashes=False)
def UserPut(user_id):
    """documentation of this method"""
    if not storage.get(User, user_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    dataObj = request.get_json()
    if not dataObj:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(User, user_id)
    for key, value in dataObj.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(obj, key, value)
    return make_response(jsonify(obj.to_dict()), 200)
