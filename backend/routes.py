from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))


######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """return length of data"""
    if data:        
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    all_urls=[]
    for each in data:
        urls=each["pic_url"]
        all_urls.append(each)
    return (all_urls, 200)
   

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for each in data:
        if id == each["id"]:
            return (each,200)
    return ({"message":"Error Invalid Id"},404)
        
    
######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    pix=request.json    
    for pic in data:
        if pix["id"] == pic["id"]:
            return {"Message":f"picture with id {pix['id']} already present"},302
    data.append(pix)
    return pix, 201
        

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pics=request.json
    for each in data:
        if each["id"] == id:
            each["id"] = pics["id"]
            each["pic_url"] = pics["pic_url"]
            each["event_country"] = pics["event_country"]
            each["event_state"] = pics["event_state"]
            each["event_city"] = pics["event_city"]
            each["event_date"] = pics["event_date"]    
            return pics, 200
    return {"message":"picture not found"}, 404

    

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for each in data:
        if each["id"] == id:
            indx = data.index(each)
            data.pop(indx)
            return {}, 204
    return {"message": "picture not found"}, 404



    
