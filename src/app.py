"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
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


# OBTENER TODOS LOS MIEMBROS
@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body)

# AÑADIR UN MIEMBRO
@app.route('/members', methods=['POST'])
def add_member():
    request_body = request.json
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.add_member(request_body)
    response_body = {
       
        "family": members
    }   
    return jsonify(response_body)
# @app.route('/user', methods=['POST'])
# def create_user():
#     request_body=request.json
#     user_query = User.query.filter_by(email=request_body["email"]).first()
#     if user_query is None:

#         user = User(email=request_body["email"], 
#         password=request_body["password"],name=request_body["name"])
#         db.session.add(user)
#         db.session.commit()
  
#         response_body = {
#             "msg": "El usuario ha sido creado con éxito",

#         }

#         return jsonify(response_body), 200
#     else:
#         return jsonify({"msg":"Usuario ya existe"}), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
