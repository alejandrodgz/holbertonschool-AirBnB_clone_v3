#!/usr/bin/python3
"""new amenities module"""

from api.v1.views import app_views
from flask import jsonify, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def allAmenities():
    """new comment"""
    listAmenities = [amenities.to_dict() for amenities
                     in storage.all(Amenity).values()]
    return listAmenities


@app_views.route('amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenitiesById(amenity_id):
    """new comment"""
    if not storage.get(Amenity, amenity_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    return jsonify(storage.get(Amenity, amenity_id).to_dict())


@app_views.route('amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenityDelete(amenity_id):
    """new comment"""
    if not storage.get(Amenity, amenity_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    obj = storage.get(Amenity, amenity_id)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenityPost():
    """new comment"""
    dataObj = request.get_json()
    if not dataObj:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in dataObj:
        return make_response(jsonify({"error": "Missing name"}), 400)
    newObj = Amenity()
    for key, value in dataObj.items():
        setattr(newObj, key, value)
    storage.new(newObj)
    storage.save()
    return make_response(jsonify(newObj.to_dict()), 201)


@app_views.route('amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def AmenityPut(amenity_id):
    """new comment"""
    if not storage.get(Amenity, amenity_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    obj = storage.get(Amenity, amenity_id)
    dataUpdate = request.get_json()
    if not dataUpdate:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in dataUpdate:
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj, key, value)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
