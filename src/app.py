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
from models import db, User
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

@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

@app.route('/user', methods=['POST'])
def create_user():

    request_body_user =  request.get_json()

    earth = User(first_name=request_body_user["first_name"], email=request_body_user["email"], password=request_body_user["password"])
    db.session.add(earth)
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

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
