#!/usr/bin/python3
"""documentation of this module must be here"""

from api.v1.views import app_views
from flask import jsonify, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def placesByCity(city_id):
    """documentation of this method must be here"""

    if not storage.get(City, city_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    city = storage.get(City, city_id)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def placeById(place_id):
    """documentation of this method must be here"""

    if not storage.get(Place, place_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    return jsonify(storage.get(Place, place_id).to_dict())


@app_views.route("/places/<place_id>",
                 methods=['DELETE'], strict_slashes=False)
def placeDelete(place_id):
    """documentation of this method must be here"""

    if not storage.get(Place, place_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    obj = storage.get(Place, place_id)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places",
                 methods=['POST'], strict_slashes=False)
def placesState(city_id):
    """documentation of this method must be here"""
    
    objData = request.get_json()
    if not storage.get(City, city_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    if not objData:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in objData:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if not storage.get(User, objData["user_id"]):
        return make_response(jsonify({"error": "Not Found"}), 404)
    if "name" not in objData:
        return make_response(jsonify({"error": "Missing name"}), 400)
    objData["city_id"] = city_id
    newObj = Place()
    for key, value in objData.items():
        setattr(newObj, key, value)
    storage.new(newObj)
    storage.save()
    return make_response(jsonify(newObj.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def placePut(place_id):
    """documentation of this method must be here"""
    if not storage.get(Place, place_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    dataUpd = request.get_json()
    if not dataUpd:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Place, place_id)
    for key, value in dataUpd.items():
        if key not in ['id', 'user_id',
                       'city_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)