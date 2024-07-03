"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.models.base import Base
from src.persistence.repository import Repository

import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model, Base):
    """User representation"""
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self) -> str:
        """User representation"""
        return f"<User {self.username}>"

    def to_dict(self) -> dict:
        """Dictionary representation of User"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Place(db.Model, Base):
    """Place representation"""
    name = db.Column(db.String(80), nullable=False)
    city_id = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    price_per_night = db.Column(db.Integer, nullable=False)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    number_of_bathrooms = db.Column(db.Integer, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    host_id = db.Column(db.String(80), nullable=False)
    amenities = db.relationship("Amenity", secondary="place_amenities")
    reviews = db.relationship("Review", backref="place")
    photos = db.relationship("Photo", backref="place")
    bookings = db.relationship("Booking", backref="place")

    def __repr__(self) -> str:
        """Place representation"""
        return f"<Place {self.name}>"

    def to_dict(self) -> dict:
        """Dictionary representation of Place"""
        return {
            "id": self.id,
            "name": self.name,
            "city_id": self.city_id,
            "user_id": self.user_id,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "price_per_night": self.price_per_night,
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "max_guests": self.max_guests,
            "host_id": self.host_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Amenity(db.Model, Base):
    """Amenity representation"""
    name = db.Column(db.String(80), nullable=False)
    place_amenities = db.relationship("PlaceAmenity", backref="amenity")
    places = db.relationship("Place", secondary="place_amenities")
    users = db.relationship("User", secondary="user_amenities")
    bookings = db.relationship("Booking", backref="amenity")

    def __repr__(self) -> str:
        """Amenity representation"""
        return f"<Amenity {self.name}>"

    def to_dict(self) -> dict:
        """Dictionary representation of the Amenity"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class City(db.Model, Base):
    """City representation"""
    name = db.Column(db.String(80), nullable=False)
    country_code = db.Column(db.String(80), nullable=False)
    places = db.relationship("Place", backref="city")
    users = db.relationship("User", backref="city")
    reviews = db.relationship("Review", backref="city")
    bookings = db.relationship("Booking", backref="city")

    def __repr__(self) -> str:
        """City representation"""
        return f"<City {self.name}>"

    def to_dict(self) -> dict:
        """Dictionary representation of the City"""
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Country(db.Model, Base):
    """Country representation"""
    name = db.Column(db.String(80), nullable=False)
    code = db.Column(db.String(80), nullable=False)
    cities = db.relationship("City", backref="country")
    users = db.relationship("User", backref="country")
    reviews = db.relationship("Review", backref="country")
    bookings = db.relationship("Booking", backref="country")

    def __repr__(self) -> str:
        """Country representation"""
        return f"<Country {self.name}>"

    def to_dict(self) -> dict:
        """Dictionary representation of the Country"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Review(db.Model, Base):
    """Review representation"""
    place_id = db.Column(db.String(80), db.ForeignKey("place.id"),
                         nullable=False)
    user_id = db.Column(db.String(80), db.ForeignKey("user.id"),
                        nullable=False)
    comment = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<{self.__class__.__name__} {self.id}>"

    def to_dict(self) -> dict:
        """Dictionary representation of Review"""
        return {
            "id": self.id,
            "place_id": self.place_id,
            "user_id": self.user_id,
            "comment": self.comment,
            "rating": self.rating,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class DBRepository(Repository):
    """Database Repository class to handle database interactions"""

    def __init__(self) -> None:
        self.db = db

    def get_all(self, model_name: str) -> list:
        model = globals().get(model_name)
        return model.query.all()

    def get(self, model_name: str, obj_id: str) -> Base | None:
        model = globals().get(model_name)
        return model.query.get(obj_id)

    def reload(self) -> None:
        pass

    def save(self, obj: Base) -> None:
        self.db.session.add(obj)
        self.db.session.commit()

    def update(self, obj: Base) -> Base | None:
        self.db.session.merge(obj)
        self.db.session.commit()

    def delete(self, obj: Base) -> bool:
        self.db.session.delete(obj)
        self.db.session.commit()
        return True


class DataManager:
    """Data Manager class to handle both
    file-based and database interactions"""

    def __init__(self, db_repository: DBRepository,
                 file_storage_path: str = 'data.json'):
        self.db_repository = db_repository
        self.file_storage_path = file_storage_path

    def _read_file(self):
        if not os.path.exists(self.file_storage_path):
            return {}
        with open(self.file_storage_path, 'r') as file:
            return json.load(file)

    def _write_file(self, data):
        with open(self.file_storage_path, 'w') as file:
            json.dump(data, file, indent=4)

    def save_user(self, user):
        if app.config['USE_DATABASE']:
            self.db_repository.save(user)
        else:
            data = self._read_file()
            data['users'] = data.get('users', [])
            data['users'].append(user.to_dict())
            self._write_file(data)

    def get_user(self, user_id):
        if app.config['USE_DATABASE']:
            return self.db_repository.get('User', user_id)
        else:
            data = self._read_file()
            users = data.get('users', [])
            return next((user for user in users if user['id'] == user_id),
                        None)

    def get_all_users(self):
        if app.config['USE_DATABASE']:
            return self.db_repository.get_all('User')
        else:
            data = self._read_file()
            return data.get('users', [])

    def update_user(self, user):
        if app.config['USE_DATABASE']:
            return self.db_repository.update(user)
        else:
            data = self._read_file()
            users = data.get('users', [])
            for i, u in enumerate(users):
                if u['id'] == user.id:
                    users[i] = user.to_dict()
                    break
            self._write_file(data)
            return user

    def delete_user(self, user_id):
        if app.config['USE_DATABASE']:
            user = self.db_repository.get('User', user_id)
            if user:
                return self.db_repository.delete(user)
            return False
        else:
            data = self._read_file()
            users = data.get('users', [])
            users = [user for user in users if user['id'] != user_id]
            data['users'] = users
            self._write_file(data)
            return True
