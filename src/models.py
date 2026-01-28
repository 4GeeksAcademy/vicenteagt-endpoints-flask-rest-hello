from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship 

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

#StarWars DB

class Users_StarWars(db.Model):
    __tablename__ = 'users_starwars'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    #relation user_favorites_characters
    user_like_character: Mapped [list['User_Favorites_Characters']] = relationship(back_populates = 'user_favorites_character')
    #relation user_favorites_planets
    user_like_planet: Mapped [list['User_Favorites_Planets']] = relationship(back_populates = 'user_favorites_planets')
    #relation user_favorites_starships
    user_like_starship: Mapped [list['User_Favorites_Starships']] = relationship(back_populates = 'user_favorites_starships')

    def __repr__(self):
        return f'Usuario: {self.name}'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password

        }

class Characters_StarWars(db.Model):
    __tablename__ = 'characters_starwars'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    specie: Mapped[str] = mapped_column(String(30), nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    #relation planets_starwars
    planet_habit: Mapped [list['Planets_StarWars']] = relationship(back_populates = 'character_for_planet')
    #relation user_favorites_characters
    user_characters_favorites: Mapped [list['User_Favorites_Characters']] = relationship(back_populates = 'characters_favorites')

    def __repr__(self):
        return f'Character: {self.name}'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "specie": self.specie,
            "gender": self.gender,
            "height": self.height,
            }
    
class Planets_StarWars(db.Model):
    __tablename__ = 'planets_starwars'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    appearances: Mapped[str] = mapped_column(String(300), nullable=False)
    species_types: Mapped[str] = mapped_column(String(30), nullable=False)
    #relation characters_starwars
    natives_characters: Mapped[int] = mapped_column(ForeignKey('characters_starwars.id'))
    character_for_planet: Mapped['Characters_StarWars'] = relationship(back_populates = 'planet_habit')
    #relation user_favorites_planets
    user_planets_favorites: Mapped [list['User_Favorites_Planets']] = relationship(back_populates = 'planets_favorites')

    def __repr__(self):
        return f'Planet: {self.name}'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "appearances": self.appearances,
            "species_types": self.species_types
            }

class Starships_StarWars(db.Model):
    __tablename__ = 'starships_starwars'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    appearances: Mapped[str] = mapped_column(String(300), nullable=False)
    affiliations: Mapped[str] = mapped_column(String(100), nullable=False)
    dimensions: Mapped[float] = mapped_column(Float, nullable=False)
    #relation user_favorites_starships
    user_starships_favorites: Mapped [list['User_Favorites_Starships']] = relationship(back_populates = 'starships_favorites')
    
    def __repr__(self):
        return f'Starship: {self.name}'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "appearances": self.appearances,
            "affiliations": self.affiliations,
            "dimensions": self.appearances}

#auxiliary dbs

class User_Favorites_Characters(db.Model):
    __tablename__ = 'user_favorites_characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    #relation user
    user_id: Mapped[int] = mapped_column(ForeignKey('users_starwars.id'))
    user_favorites_character: Mapped['Users_StarWars'] = relationship(back_populates = 'user_like_character')
    #relation characters
    characters_id: Mapped[int] = mapped_column(ForeignKey('characters_starwars.id'))
    characters_favorites: Mapped['Characters_StarWars'] = relationship(back_populates = 'user_characters_favorites')
    #relation characters

    def __repr__(self):
        return f'A: {self.user_favorites_character} le gusta el {self.characters_favorites}'
    
    def serialize(self):
        return {
            "id": self.id,
            "usuario": self.user_favorites_character,
            "characters_favorites": self.characters_favorites
            }

class User_Favorites_Planets(db.Model):
    __tablename__ = 'user_favorites_planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    #relation user
    user_id: Mapped[int] = mapped_column(ForeignKey('users_starwars.id'))
    user_favorites_planets: Mapped['Users_StarWars'] = relationship(back_populates = 'user_like_planet')
    #relation planets 
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets_starwars.id'))
    planets_favorites: Mapped['Planets_StarWars'] = relationship(back_populates = 'user_planets_favorites')

    def __repr__(self):
        return f'A: {self.user_favorites_planets} le gusta el {self.planets_favorites}'
    
    def serialize(self):
        return {
            "id": self.id,
            "usuario": self.user_favorites_planets,
            "planets_favorites": self.planets_favorites
            }
    
class User_Favorites_Starships(db.Model):
    __tablename__ = 'user_favorites_starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    #relation user
    user_id: Mapped[int] = mapped_column(ForeignKey('users_starwars.id'))
    user_favorites_starships: Mapped['Users_StarWars'] = relationship(back_populates = 'user_like_starship')
    #relation starships
    starship_id: Mapped[int] = mapped_column(ForeignKey('starships_starwars.id'))
    starships_favorites: Mapped['Starships_StarWars'] = relationship(back_populates = 'user_starships_favorites')

    def __repr__(self):
        return f'A: {self.user_favorites_starships} le gusta la {self. starships_favorites}'
    
    def serialize(self):
        return {
            "id": self.id,
            "usuario": self.user_favorites_starships,
            "starships_favorites": self.starships_favorites
            }