from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(12), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=True)

    planet_favorites: Mapped[list["FavoritePlanet"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    character_favorites: Mapped[list["FavoriteCharacter"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "favorite_characters": [fav.character.serialize() for fav in self.character_favorites],
             "favorite_planets": [fav.planet.serialize() for fav in self.planet_favorites]
        }


class Character(db.Model):
    __tablename__ = "character"

    character_id: Mapped[int] = mapped_column(primary_key=True)
    character_homeworld: Mapped[str] = mapped_column(String(250), nullable=False)
    character_name: Mapped[str] = mapped_column(String(250))
    character_skill: Mapped[str] = mapped_column(String(250), nullable=False)

    character_favorites: Mapped[list["FavoriteCharacter"]] = relationship(back_populates="character", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Character {self.character_name}>"

    def serialize(self):
        return {
            "character_id": self.character_id,
            "character_name": self.character_name,
            "character_skill": self.character_skill
        }


class Planet(db.Model):
    __tablename__ = "planet"

    planet_id: Mapped[int] = mapped_column(primary_key=True)
    planet_population: Mapped[int] = mapped_column(nullable=False)
    planet_diameter: Mapped[int] = mapped_column(nullable=False)
    planet_climate: Mapped[str] = mapped_column(String(250), nullable=False)
    planet_name: Mapped[str] = mapped_column(String(250))

    planet_favorites: Mapped[list["FavoritePlanet"]] = relationship(back_populates="planet", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Planet {self.planet_name}>"

    def serialize(self):
        return {
            "planet_id": self.planet_id,
            "planet_name": self.planet_name,
            "planet_climate": self.planet_climate
        }


class FavoriteCharacter(db.Model):
    __tablename__ = "favorite_character"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.character_id"))

    user: Mapped["User"] = relationship(back_populates="character_favorites")
    character: Mapped["Character"] = relationship(back_populates="character_favorites")

    def __repr__(self):
        return f"<FavoriteCharacter {self.user_id}>"

    def serialize(self):
        return {
            
            "id": self.id,
            "user": self.user.id,
            "character_id": self.character_id,
        }


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.planet_id"))

    user: Mapped["User"] = relationship(back_populates="planet_favorites")
    planet: Mapped["Planet"] = relationship(back_populates="planet_favorites")

    def __repr__(self):
        return f"<FavoritePlanet {self.user_id}>"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "planet_id": self.planet_id,
        }

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
