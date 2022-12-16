#!/usr/bin/python3
"""this is where the file should be documented"""

from api.v1.views import app_views
from flask import jsonify, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviewsPlace(place_id):
    """documentation of this method must be here"""
    if not storage.get(Place, place_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    place = storage.get(Place, place_id)
    return jsonify([reviews.to_dict() for reviews in place.reviews])


@app_views.route('reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def reviewId(review_id):
    """documentation of this method must be here"""
    if not storage.get(Review, review_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    return jsonify(storage.get(Review, review_id).to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def reviewDelete(review_id):
    """documentation of this method must be here"""
    if not storage.get(Review, review_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    obj = storage.get(Review, review_id)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def reviewPost(place_id):
    """documentation of this method must be here"""
    objData = request.get_json()
    if not storage.get(Place, place_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    if not objData:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in objData:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if not storage.get(User, objData["user_id"]):
        return make_response(jsonify({"error": "Not Found"}), 404)
    if "text" not in objData:
        return make_response(jsonify({"error": "Missing text"}), 400)
    objData["place_id"] = place_id
    newObj = Review()
    for key, value in objData.items():
        setattr(newObj, key, value)
    storage.new(newObj)
    storage.save()
    return make_response(jsonify(newObj.to_dict()), 201)


@app_views.route('reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def reviewPut(review_id):
    """documentation of this method must be here"""
    if not storage.get(Review, review_id):
        return make_response(jsonify({"error": "Not Found"}), 404)
    dataUpd = request.get_json()
    if not dataUpd:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Review, review_id)
    for key, value in dataUpd.items():
        if key not in ['id', 'user_id',
                       'place_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
