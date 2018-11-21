from flask import jsonify, request, make_response
from collective_todo import app, db
from collective_todo.routes.auth import token_required
from collective_todo.models.User import User
from collective_todo.models.Group import Group
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/user', methods=['GET'])
@token_required
def get_users(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function'})

    users = User.query.all()
    output = []
    for user in users:
        user_data = {
            'public_id': user.public_id,
            'name': user.name,
            'password': user.password,
            'admin': user.admin,
        }
        output.append(user_data)
    return jsonify({'users': output})

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_user_by_id(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message':'No user found!'})

    user_data = {
        'public_id': user.public_id,
        'name': user.name,
        'password': user.password,
        'admin': user.admin,
    }

    return jsonify({'user': user_data})

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function'})

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        public_id=str(uuid.uuid4()),
        name=data['name'],
        password=hashed_password,
        admin=False,
    )

    db.session.add(new_user)
    db.session.flush()

    new_group = Group(
        name=data['name'],
        owner=new_user,
    )

    new_group.users.append(new_user)
    db.session.add(new_group)
    db.session.commit()
    return jsonify({'message': 'new user created'})

@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message':'No user found!'})

    user.admin = True
    db.session.commit()
    return jsonify({'message': 'The user has been promoted!'})

@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message':'No user found!'})

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'The user has been deleted!'})
