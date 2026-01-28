import os
from flask_admin import Admin
from models import db, User, Users_StarWars, Characters_StarWars, Planets_StarWars, Starships_StarWars, User_Favorites_Characters, User_Favorites_Planets, User_Favorites_Starships
from flask_admin.contrib.sqla import ModelView

class UserModelView(ModelView):
    column_auto_select_related = True 
    column_list = ['id', 'email', 'password', 'is_active']
                   
class Users_StarWarsModelView(ModelView):
    column_auto_select_related = True 
    column_list = ['id','name', 'email', 'password', 'user_like_character',
                   'user_like_planet','user_like_starship' ] 
    
class Characters_StarWarsModelView(ModelView):
    column_auto_select_related = True 
    column_list = ['id','name', 'specie', 'gender', 'height', 'planet_habit',
                   'user_characters_favorites']

class Planets_StarWarsModelView(ModelView):
    column_auto_select_related = True 
    column_list = ['id', 'name', 'appearances', 'species_types', 'natives_characters',
                  'character_for_planet', 'user_planets_favorites']
    
class Starships_StarWarsModelView(ModelView):
    column_auto_select_related = True 
    column_list = ['id', 'name', 'appearances', 'affiliations', 'dimensions',
                   'user_starships_favorites']
    
#db relations
class User_Favorites_CharactersModelView(ModelView):
    column_auto_select_related = True 
    column_list = ['id', 'user_id', 'user_favorites_character', 'characters_id', 'characters_favorites']

class User_Favorites_PlanetsModelView(ModelView):
    column_auto_select_related = True 
    column_list = ['id', 'user_id', 'user_favorites_planets', 'planet_id', 'planets_favorites']

class User_Favorites_StarshipsModelView(ModelView):
    column_auto_select_related = True 
    column_list = ['id', 'user_id', 'user_favorites_starships', 'starship_id', 'starships_favorites']
                   
def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(Users_StarWarsModelView(Users_StarWars, db.session))
    admin.add_view(Characters_StarWarsModelView(Characters_StarWars, db.session))
    admin.add_view(Planets_StarWarsModelView(Planets_StarWars, db.session))
    admin.add_view(Starships_StarWarsModelView(Starships_StarWars, db.session))
    #db relations
    admin.add_view(User_Favorites_CharactersModelView(User_Favorites_Characters, db.session))
    admin.add_view(User_Favorites_PlanetsModelView(User_Favorites_Planets, db.session))
    admin.add_view(User_Favorites_StarshipsModelView(User_Favorites_Starships, db.session))



    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))