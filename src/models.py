from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True, default=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    eye_color = db.Column(db.String(20), unique=False, nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
  
    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender
            # do not serialize the password, its a security breach
        }
    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, nullable=True)
    planet_id = db.Column(db.Integer, unique=False, nullable=True)
    user_id = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Favorite %r>' % self.character_id

    def serialize(self):
        return {
            "id": self.id,
            "character_id": self.character_id,
            "planet_id": self.planet_id
            # do not serialize the password, its a security breach
        }