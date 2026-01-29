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
from models import db, User, Users_StarWars, Characters_StarWars, Planets_StarWars, Starships_StarWars, User_Favorites_Characters, User_Favorites_Planets, User_Favorites_Starships
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

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

#endpoints starwars

#enpoint get all characters
@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Characters_StarWars.query.all()
    characters_serialized = []
    for character in characters:
        characters_serialized.append(character.serialize())
    return jsonify({'data': characters_serialized}), 200

#endpoint get character fo id
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters_StarWars.query.get(character_id)
    character_serialized = character.serialize()
    return jsonify({'data': character_serialized}),200

#enpoint get all planets
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets_StarWars.query.all()
    planets_serialized = []
    for planet in planets:
        planets_serialized.append(planet.serialize())
    return jsonify({'data': planets_serialized}), 200

#endpoint get planet fo id
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets_StarWars.query.get(planet_id)
    planet_serialized = planet.serialize()
    return jsonify({'data': planet_serialized}),200

#endpoint get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = Users_StarWars.query.all()
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
    return jsonify({'data': users_serialized}), 200

#endpoint get all favorites for user id
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = Users_StarWars.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'El usuario {user_id}, no existe'}), 404
    favorites_characters_serialized = []
    for favorite in user.user_like_character:
        favorites_characters_serialized.append(favorite.characters_favorites.serialize())
    favorites_planets_serialized = []
    for favorite in user.user_like_planet:
        favorites_planets_serialized.append(favorite.planets_favorites.serialize())
    favorites_starships_serialized = []
    for favorite in user.user_like_starship:
        favorites_starships_serialized.append(favorite.starships_favorites.serialize())

    return jsonify({'Personajes favoritos': favorites_characters_serialized,
                    'Planetas favoritos': favorites_planets_serialized,
                    'Staships favoritas': favorites_starships_serialized
                    }),200
    
#endpoint post add a new planet favorite to a user id
@app.route('/favorite/planet/<int:planet_id>/user/<int:user_id>', methods=['POST'])  
def add_new_favorite_planet(user_id, planet_id):
    user = Users_StarWars.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'Usuario {user_id} no encontrado'}), 404
    planet= Planets_StarWars.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': f'Planeta {planet_id} no encontrado'}), 404
    
    new_favorite = User_Favorites_Planets()
    new_favorite.user_favorites_planets = user
    new_favorite.planets_favorites = planet
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify(f'Se ha agregado correctamente el {planet} al {user}'), 200

#endpoint post add a new character favorite to a user id
    
@app.route('/favorite/character/<int:character_id>/user/<int:user_id>', methods=['POST'])  
def add_new_favorite_character(user_id, character_id):
    user = Users_StarWars.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'Usuario {user_id} no encontrado'}), 404
    character= Characters_StarWars.query.get(character_id)
    if character is None:
        return jsonify({'msg': f'Personaje {character_id} no encontrado'}), 404
    
    new_favorite_character = User_Favorites_Characters()
    new_favorite_character.user_favorites_character = user
    new_favorite_character.characters_favorites = character
    db.session.add(new_favorite_character)
    db.session.commit()
    
    return jsonify(f'Se ha agregado correctamente el {character} al {user}'), 200

#endpoint delete a planet favorite to a user id
@app.route('/favorite/planet/<int:planet_id>/user/<int:user_id>', methods=['DELETE'])  
def delete_planet(user_id, planet_id):
    user = Users_StarWars.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'Usuario {user_id} no encontrado'}), 404
    planet= Planets_StarWars.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': f'Planeta {planet_id} no encontrado'}), 404
    
    find_relation = User_Favorites_Planets.query.filter_by(
        user_favorites_planets = user,
        planets_favorites = planet). first()
     
    if find_relation is None:
        return jsonify ({'msg': 'La relación no existe'}), 404
    
    db.session.delete(find_relation)
    db.session.commit()

    return jsonify(f'Se ha eliminado correctamente el {planet} al {user}'), 200

#endpoint delete a character favorite to a user id
@app.route('/favorite/character/<int:character_id>/user/<int:user_id>', methods=['DELETE'])  
def delete_character(user_id, character_id):
    user = Users_StarWars.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'Usuario {user_id} no encontrado'}), 404
    character= Characters_StarWars.query.get(character_id)
    if character is None:
        return jsonify({'msg': f'Personaje {character_id} no encontrado'}), 404
    
    find_relation = User_Favorites_Characters.query.filter_by(
        user_favorites_character = user,
        characters_favorites = character). first()
     
    if find_relation is None:
        return jsonify ({'msg': 'La relación no existe'}), 404
    
    db.session.delete(find_relation)
    db.session.commit()

    return jsonify(f'Se ha eliminado correctamente el {character} al {user}'), 200

#adicionals endpoints
#endpoint post add a new user in users
@app.route('/adduser', methods=['POST'])  
def add_new_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Necesitas llenar el body'}),400
    if 'name' not in body:
        return jsonify({'msg': 'Necesitas llenar el campo name'}),400
    if 'email' not in body:
        return jsonify({'msg': 'Necesitas llenar el campo email'}),400
    if 'password' not in body:
        return jsonify({'msg': 'Necesitas llenar el campo paswword'}),400
    new_user = Users_StarWars()
    new_user.name = body['name']
    new_user.email = body['email']
    new_user.password = body['password']
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': f'Se ha agregado a {new_user.name} a la base de datos'}), 200

#endpont put edit user information
@app.route('/edituser/<int:user_id>', methods=['PUT'])  
def edit_information_user(user_id):
    user = Users_StarWars.query.get(user_id)
    if user is None:
        return jsonify({'msg': f'Usuario {user_id} no encontrado'}), 404

    body = request.get_json(silent=True)
    if 'name' in body:
        user.name = body['name']
    if 'email' in body:
        user.email = body['email']
    if 'password' in body:
        user.password = body['password']
    db.session.commit()

    return jsonify({'msg': f'Información de {user.name} actualizada'})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
