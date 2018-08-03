import json

from flask import Blueprint
from flask import jsonify
from flask import request

from controller import BeritaController
from exceptions import BadRequest

beritaController = BeritaController()

bp = Blueprint(__name__, "berita")

@bp.route("/berita", methods=["GET"])
def get_berita():
    berita_type = request.args.get("type")
    print(berita_type)

    if not berita_type:
        raise BadRequest("type is required", 200, 1)

    result = beritaController.get_berita(berita_type)

    response = {"error": 0, "message": "success", "data": result}

    return jsonify(response)

@bp.route("/berita", methods=["POST"])
def create_berita():
    berita_object = request.form.get("berita_object")
    #berita_object = request.data
    #print(berita_object)

    try:
        berita_object_json = json.loads(berita_object)
    except:
        raise BadRequest("berita_object is missing or error format", 200, 1)

    try:
        berita_title = berita_object_json['title']
        berita_category = berita_object_json['category']
        berita_type = berita_object_json['type']
        berita_content = berita_object_json['content']
        berita_slug = berita_object_json['slug']
    except:
        raise BadRequest("title, slug, category, type or content is missing",
                         200, 1)

    params = {
        "berita_title": berita_title,
        "berita_slug": berita_slug,
        "berita_category": berita_category,
        "berita_type": berita_type,
        "berita_content": berita_content,
    }

    result = beritaController.create_berita(**params)

    response = {"message": "success", "error": 0, "data": result}

    return jsonify(response)

@bp.route("/berita/<berita_slug>", methods=["GET"])
def get_single_berita(berita_slug):
    berita_type = request.args.get("type")

    if not berita_type:
        raise BadRequest("type is missing", 200, 1)

    result = beritaController.get_berita_by_slug(berita_slug, berita_type)

    response = {"error": 0, "message": "success", "data": result}

    return jsonify(response)

@bp.route("/berita/<berita_id>", methods=["PUT"])
def update_single_berita(berita_id):
    berita_object = request.form.get("berita_object")

    try:
        berita_object_json = json.loads(berita_object)
    except:
        raise BadRequest("berita_object is missing or error format", 200, 1)

    result = beritaController.update_berita(berita_id, berita_object_json)

    response = {"error": 0, "message": "success", "data": result}

    return jsonify(response)

@bp.route("/berita/<berita_id>", methods=["DELETE"])
def delete_single_berita(berita_id):
    beritaController.delete_berita(berita_id)

    response = {"error": 0, "message": "success", "data": {}}

    return jsonify(response)