"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#USER
@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

@app.route('/user', methods=['POST'])
def create_user():

    request_body_user =  request.get_json()

    change = User(first_name=request_body_user["first_name"], email=request_body_user["email"], password=request_body_user["password"])
    db.session.add(change)
    db.session.commit()

    return jsonify(request_body_user), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', state_code=404)

    db.session.delete(user1)
    db.session.commit()    

    return jsonify("ok"), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):

   request_body_user =  request.get_json()

   user1 = User.query.get(user_id)
   if user1 is None:
    raise APIException('User not found', state_code=404)
   
   if "username" in request_body_user:
        user1.username = body["username"]
   if "email" in request_body_user:
        user1.email = body["email"]
   if "first_name" in request_body_user:
        user1.first_name = request_body_user["first_name"]
   db.session.commit()

   return jsonify(request_body_user), 200

#CHARACTER

@app.route('/character', methods=['GET'])
def get_characters():

    characters = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), characters))

    return jsonify(all_characters), 200

@app.route('/character', methods=['POST'])
def post_character():

    request_body_user =  request.get_json()

    change = Character(name=request_body_user["name"], eye_color=request_body_user["eye_color"], birth_year=request_body_user["birth_year"], gender=request_body_user["gender"])
    
    db.session.add(change)
    db.session.commit()

    return jsonify(request_body_user), 200


#PLANET

@app.route('/planet', methods=['GET'])
def get_planets():

    planet = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), planet))

    return jsonify(all_planets), 200

@app.route('/planet', methods=['POST'])
def post_planets():

    request_body_user =  request.get_json()

    change = Planet(name=request_body_user["name"], diameter=request_body_user["diameter"], climate=request_body_user["climate"])
    
    db.session.add(change)
    db.session.commit()

    return jsonify(request_body_user), 200


#FAVORITE

@app.route('/user/favorite', methods=['GET'])
def get_favorites():

    favorite = Favorite.query.all()
    all_favorites = list(map(lambda x: x.serialize(), favorite))

    return jsonify(all_favorites), 200

@app.route('/user/favorite', methods=['POST'])
def post_favorites():

    request_body_user =  request.get_json()

    change = Favorite(character_id=request_body_user["character_id"], planet_id=request_body_user["planet_id"])
    
    db.session.add(change)
    db.session.commit()

    return jsonify(request_body_user), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
