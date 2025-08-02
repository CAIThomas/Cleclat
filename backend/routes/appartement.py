# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from ..models import db, Appartement, User, UserAppartement
from datetime import datetime

appartements_bp = Blueprint('appartements', __name__)
# 🔹 Récupérer tous les appartements
@appartements_bp.route('/appartements', methods=['GET'])
def get_appartements():
    appartements = Appartement.query.all()
    result = []
    for app in appartements:
        result.append({
            'id': app.id,
            'title': app.title,
            'address': app.address,
            'description': app.description,
            'photos': app.photos or [],
            'owner_id': app.owner_id
        })
    return jsonify(result)


# 🔹 Ajouter un appartement
@appartements_bp.route('/appartements', methods=['POST'])
def add_appartement():
    data = request.get_json()
    required_fields = ['title', 'address', 'owner_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    owner = User.query.get(data['owner_id'])
    if not owner or owner.role != 'loueur':
        return jsonify({'error': 'Owner must be a valid loueur'}), 400

    description = data.get('description')
    photos = data.get('photos', [])

    if not isinstance(photos, list):
        return jsonify({'error': 'Photos must be a list of URLs'}), 400

    new_app = Appartement(
        title=data['title'],
        address=data['address'],
        description=description,
        photos=photos,
        owner_id=data['owner_id']
    )
    db.session.add(new_app)
    db.session.commit()
    return jsonify({'message': 'Appartement added', 'id': new_app.id}), 201


# 🔹 Mettre à jour un appartement
@appartements_bp.route('/appartements/<int:id>', methods=['PUT'])
def update_appartement(id):
    app = Appartement.query.get_or_404(id)
    data = request.get_json()

    if 'title' in data:
        app.title = data['title']
    if 'address' in data:
        app.address = data['address']
    if 'description' in data:
        app.description = data['description']
    if 'photos' in data:
        if not isinstance(data['photos'], list):
            return jsonify({'error': 'Photos must be a list'}), 400
        app.photos = data['photos']

    db.session.commit()
    return jsonify({'message': 'Appartement updated successfully'})
