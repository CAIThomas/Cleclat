# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from models import db, User, Appartement, UserAppartement
from datetime import datetime
from sqlalchemy.orm import joinedload

users_bp = Blueprint('users', __name__)

# 🔹 Récupérer tous les utilisateurs
@users_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "birth_date": user.birth_date.isoformat() if user.birth_date else None,
            "role": user.role
        })
    return jsonify(result)

# 🔹 Récupérer un utilisateur par ID
@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'birth_date': user.birth_date.strftime('%Y-%m-%d') if user.birth_date else None,
        'email': user.email,
        'role': user.role
    })

# 🔹 Ajouter un utilisateur
@users_bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()

    required_fields = ['first_name', 'last_name', 'email', 'password', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    birth_date = None
    if 'birth_date' in data:
        try:
            birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format, expected YYYY-MM-DD'}), 400

    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password'],
        birth_date=birth_date,
        role=data['role']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

# 🔹 Mettre à jour un utilisateur
@users_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'email' in data:
        user.email = data['email']
    if 'role' in data:
        user.role = data['role']
    if 'birth_date' in data:
        try:
            user.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400

    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

# 🔹 Supprimer un utilisateur
@users_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# 🔹 Connexion utilisateur simple
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401

    return jsonify({
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'birth_date': user.birth_date.isoformat() if user.birth_date else None,
        'role': user.role
    })

# 🔹 Appartements loués par un utilisateur (si locataire)
@users_bp.route('/users/<int:id>/appartements', methods=['GET'])
def get_user_appartements(id):
    locations = UserAppartement.query.filter_by(user_id=id).all()
    result = []
    for l in locations:
        app = Appartement.query.get(l.appartement_id)
        result.append({
            'appartement_id': app.id,
            'title': app.title,
            'rented_on': l.rented_on.strftime('%Y-%m-%d') if l.rented_on else None
        })
    return jsonify(result)
