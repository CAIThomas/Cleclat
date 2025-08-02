# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

db = SQLAlchemy()

# 🔁 Table d'association : historique de location
class UserAppartement(db.Model):
    __tablename__ = 'user_appartement'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    appartement_id = db.Column(db.Integer, db.ForeignKey('appartement.id'), nullable=False)
    rented_at = db.Column(db.DateTime, default=datetime.utcnow)
    returned_at = db.Column(db.DateTime, nullable=True)

    user = relationship("User", back_populates="user_appartements")
    appartement = relationship("Appartement", back_populates="user_appartements")

class Appartement(db.Model):
    __tablename__ = 'appartement'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    photos = db.Column(JSON, nullable=True)  # liste de strings (URLs)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    owner = relationship("User", back_populates="owned_appartements")
    user_appartements = relationship("UserAppartement", back_populates="appartement", cascade="all, delete-orphan")

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    password = db.Column(db.String(200), nullable=False)

    # Rôle : 'locataire', 'proprietaire', ...
    role = db.Column(db.String(20), nullable=False, default='locataire')

    # Appartements possédés (propriétaire)
    owned_appartements = relationship("Appartement", back_populates="owner")

    # Locations (historique)
    user_appartements = relationship("UserAppartement", back_populates="user", cascade="all, delete-orphan")

    # Appartements actuellement loués (view only)
    rented_appartements = relationship("Appartement", secondary="user_appartement", viewonly=True)
