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
from models import db, User, Character, Planet, FavoriteCharacter, FavoritePlanet
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify("no user found")
    db.session.delete(user)
    db.session.commit()

    response ={
        "msg":"user deleted!",
        "user":user.serialize()
    }
    return jsonify(response), 200


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        username=data['username'],
        password=data['password'],
        is_active=data.get('is_active', True)
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201


@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    return jsonify([c.serialize() for c in characters]), 200


@app.route('/characters', methods=['POST'])
def create_character():
    data = request.json
    new_character = Character(
        character_homeworld=data['character_homeworld'],
        character_name=data.get('character_name', ''),
        character_skill=data['character_skill']
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201


@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200


@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.json
    new_planet = Planet(
        planet_name=data.get('planet_name', ''),
        planet_population=data['planet_population'],
        planet_diameter=data['planet_diameter'],
        planet_climate=data['planet_climate']
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

@app.route('/favorite-planets', methods=['GET'])
def get_all_favorite_planets():
    favorites = FavoritePlanet.query.all()
    return jsonify([f.serialize() for f in favorites]), 200

@app.route('/favorite-planets', methods=['POST'])
def add_favorite_planet():
    data = request.json
    user = User.query.get(data['user_id'])
    planet = Planet.query.get(data['planet_id'])

    if not user or not planet:
        return jsonify({"error": "User or Planet not found"}), 404

    favorite = FavoritePlanet(user_id=user.id, planet_id=planet.planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite-characters', methods=['GET'])
def get_all_favorite_characters():
    favorites = FavoriteCharacter.query.all()
    return jsonify([f.serialize() for f in favorites]), 200

@app.route('/favorite-characters', methods=['POST'])
def add_favorite_character():
    data = request.json
    user = User.query.get(data['user_id'])
    character = Character.query.get(data['character_id'])

    if not user or not character:
        return jsonify({"error": "User or Character not found"}), 404

    favorite = FavoriteCharacter(user_id=user.id, character_id=character.character_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite-characters/<int:id>', methods=['DELETE'])
def delete_favorite_character(id):

    favorite = FavoriteCharacter.query.get(id)
    if not favorite:
        return jsonify("no favorite found")
    fav = favorite.serialize()
    db.session.delete(favorite)
    db.session.commit()
    resp={
        "msg": "fav deleted!"
    }
    return jsonify(fav), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
