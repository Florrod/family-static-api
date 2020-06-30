"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def getOneFamilyMember(member_id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(member_id)
    return jsonify(member), 200

@app.route('/member' , methods=['POST'])
def addMember():
    requests_body= json.loads(request.data) # Para recoger solo los datos del body (objeto) y ponerlos en formato json
    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.add_member(requests_body)
    return jsonify(requests_body), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def deleteMember(member_id):

    # this is how you can use the Family datastructure by calling its methods
    member_to_show= jackson_family.get_member(member_id)
    member = jackson_family.delete_member(member_id)
    return jsonify (member_to_show), 200
    # return jsonify({"done": True}), 200 La línea 59 nos muestra el miembro elimnado y esta línea verificaría que está eliminado

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
