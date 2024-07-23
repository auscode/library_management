from flask import Blueprint, request, jsonify
from app.models import User, db
from app.utils import role_required
from werkzeug.security import generate_password_hash
from flask_jwt_extended import get_jwt_identity

users_bp = Blueprint('users', __name__)

@users_bp.route('/add', methods=['POST'])
@role_required('LIBRARIAN')
def add_member():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_member = User(username=data['username'], password=hashed_password, role='MEMBER')
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'Member added successfully!'}), 201

@users_bp.route('/<int:id>', methods=['PUT'])
@role_required('LIBRARIAN')
def update_member(id):
    data = request.get_json()
    member = User.query.get_or_404(id)
    member.username = data['username']
    if 'password' in data:
        member.password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    db.session.commit()
    return jsonify({'message': 'Member updated successfully!'}), 200

@users_bp.route('/<int:id>', methods=['DELETE'])
@role_required('LIBRARIAN')
def delete_member(id):
    member = User.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member deleted successfully!'}), 200

@users_bp.route('/', methods=['GET'])
@role_required('LIBRARIAN')
def view_members():
    members = User.query.filter_by(role='MEMBER').all()
    return jsonify([{'id': member.id, 'username': member.username} for member in members]), 200

@users_bp.route('/me', methods=['DELETE'])
@role_required('MEMBER')
def delete_own_account():
    user_identity = get_jwt_identity()
    member = User.query.filter_by(username=user_identity['username']).first_or_404()
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Account deleted successfully!'}), 200
