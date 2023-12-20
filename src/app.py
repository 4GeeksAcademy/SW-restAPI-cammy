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
        user1.username = request_body_user["username"]
   if "email" in request_body_user:
        user1.email = request_body_user["email"]
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

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):

    character1 = Character.query.get(character_id)
    if character1 is None:
        raise APIException('Character not found', state_code=404)

    db.session.delete(character1)
    db.session.commit()    

    return jsonify("Character successfully deleted"), 200

@app.route('/character/<int:character_id>', methods=['PUT'])
def update_character(character_id):

   request_body_user =  request.get_json()

   character1 = Character.query.get(character_id)
   if character1 is None:
    raise APIException('Character not found', state_code=404)
   
   if "name" in request_body_user:
        character1.name = request_body_user["name"]
   if "eye_color" in request_body_user:
        character1.eye_color = request_body_user["eye_color"]
   if "birth_year" in request_body_user:
        character1.birth_year = request_body_user["birth_year"]
   if "gender" in request_body_user:
        character1.gender = request_body_user["gender"]
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

@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):

    planet1 = Planet.query.get(planet_id)
    if planet1 is None:
        raise APIException('Planet not found', state_code=404)

    db.session.delete(planet1)
    db.session.commit()    

    return jsonify("Planet successfully deleted"), 200

@app.route('/planet/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):

   request_body_user =  request.get_json()

   planet1 = Planet.query.get(planet_id)
   if planet1 is None:
    raise APIException('Planet not found', state_code=404)
   
   if "name" in request_body_user:
        planet1.name = request_body_user["name"]
   if "diameter" in request_body_user:
        planet1.diameter = request_body_user["diameter"]
   if "climate" in request_body_user:
        planet1.climate = request_body_user["climate"]
   db.session.commit()

   return jsonify(request_body_user), 200


#FAVORITE

@app.route('/user/<int:user_id>/favorite', methods=['GET'])
def get_user_favorites(user_id):

    favorites = Favorite.query.filter_by(id=user_id).all()
    all_favorites = [favorite.serialize() for favorite in favorites]

    return jsonify(all_favorites), 200

@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def planet_favorites(user_id, planet_id):
    
    planet = Favorite.query.filter_by(planet_id=planet_id, user_id=user_id).first()
    if planet is None:
        fav_planet = Planet.query.filter_by(id=planet_id).first()
        if fav_planet is None:
            return jsonify({"error": "Planet not found"}), 401
        else: 
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                return jsonify ({"error": "User not found"}), 401 
            else:
                fav_planets = Favorite(user_id=user_id, planet_id=planet_id)

                db.session.add(fav_planets)
                db.session.commit()
    else:
        return jsonify({"error": "Planet already added"}), 201

@app.route('/user/<int:user_id>/favorite/character/<int:character_id>', methods=['POST'])
def character_favorites(user_id, character_id):

    character = Favorite.query.filter_by(character_id=character_id, user_id=user_id).first()
    if character is None:
        fav_character = Character.query.filter_by(id=character_id).first()
        if fav_character is None:
            return jsonify({"error": "Character not found"}), 401
        else: 
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                return jsonify ({"error": "User not found"}), 401 
            else:
                fav_characters = Favorite(user_id=user_id, character_id=character_id)

                db.session.add(fav_characters)
                db.session.commit()
    else:
        return jsonify({"error": "Character already added"}), 201

# DELETE
@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def planet_delete(user_id, planet_id):
    
    planet = Favorite.query.filter_by(planet_id=planet_id, user_id=user_id).first()
    if planet is None:
        fav_planet = Planet.query.filter_by(id=planet_id).first()
        if fav_planet is None:
            return jsonify({"error": "Planet not found"}), 401
        else: 
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                return jsonify ({"error": "User not found"}), 401 
            else:
                fav_planets = Favorite(user_id=user_id, planet_id=planet_id)

                db.session.delete(fav_planets)
                db.session.commit()
                return jsonify({"msg": "Favorite planet deleted successfully"}), 200
    else:
        return jsonify({"error": "Planet cannot be deleted"}), 201    

@app.route('/user/<int:user_id>/favorite/character/<int:character_id>', methods=['DELETE'])
def character_delete(user_id, character_id):    

    character = Favorite.query.filter_by(character_id=character_id, user_id=user_id).first()
    if character is None:
        fav_character = Character.query.filter_by(id=character_id).first()
        if fav_character is None:
            return jsonify({"error": "Character not found"}), 401
        else: 
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                return jsonify ({"error": "User not found"}), 401 
            else:
                fav_characters = Favorite(user_id=user_id, character_id=character_id)

                db.session.delete(fav_characters)
                db.session.commit()
                return jsonify({"msg": "Favorite character deleted successfully"}), 200
    else:
        return jsonify({"error": "Character cannot be deleted"}), 201


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
