from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

# Car-related models
class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    cars = db.relationship('Car', backref='company', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class FuelType(db.Model):
    __tablename__ = 'fuel_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    cars = db.relationship('Car', backref='fuel_type', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Engine(db.Model):
    __tablename__ = 'engines'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # V8, V12, I4, etc.
    cc = db.Column(db.Integer, nullable=True)  # Engine displacement in cc
    horsepower = db.Column(db.Integer, nullable=True)
    torque = db.Column(db.Integer, nullable=True)  # in Nm
    cars = db.relationship('Car', backref='engine', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'cc': self.cc,
            'horsepower': self.horsepower,
            'torque': self.torque
        }

class Car(db.Model):
    __tablename__ = 'cars'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    engine_id = db.Column(db.Integer, db.ForeignKey('engines.id'), nullable=True)
    fuel_type_id = db.Column(db.Integer, db.ForeignKey('fuel_types.id'), nullable=True)
    price = db.Column(db.Integer, nullable=True)  # in USD
    seats = db.Column(db.Integer, nullable=True)
    performance = db.relationship('Performance', backref='car', uselist=False, lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'company_id': self.company_id,
            'company': self.company.name if self.company else None,
            'engine_id': self.engine_id,
            'fuel_type_id': self.fuel_type_id,
            'fuel_type': self.fuel_type.name if self.fuel_type else None,
            'price': self.price,
            'seats': self.seats
        }

class Performance(db.Model):
    __tablename__ = 'performance'
    
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False, unique=True)
    top_speed = db.Column(db.Integer, nullable=True)  # in km/h
    acceleration_0_100 = db.Column(db.Float, nullable=True)  # in seconds
    
    def to_dict(self):
        return {
            'id': self.id,
            'top_speed': self.top_speed,
            'acceleration_0_100': self.acceleration_0_100
        }

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }