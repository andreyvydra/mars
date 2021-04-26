import flask
from flask import jsonify, request

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id',
                                    'surname',
                                    'name',
                                    'position',
                                    'age',
                                    'speciality',
                                    'address',
                                    'email'
                                    )) for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('id',
                                       'surname',
                                       'name',
                                       'position',
                                       'age',
                                       'speciality',
                                       'address',
                                       'email'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname',
                  'name',
                  'position',
                  'age',
                  'speciality',
                  'address',
                  'email']):
        return jsonify({'error': 'Bad request'})
    elif not isinstance(request.json['age'], int):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        position=request.json['position'],
        age=int(request.json['age']),
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email']
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users', methods=['PUT'])
def update_user():
    params_to_edit = {
        'id': None,
        'surname': None,
        'name': None,
        'position': None,
        'age': None,
        'speciality': None,
        'address': None,
        'email': None
    }

    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not any(key in params_to_edit.keys() for key in request.json):
        return jsonify({'error': 'Bad request'})
    elif not ('id' in request.json):
        return jsonify({'error': 'User id wasnt found'})
    else:
        for key in request.json:
            params_to_edit[key] = request.json[key]

    db_sess = db_session.create_session()
    user = db_sess.query(User).get(int(request.json['id']))
    if not user:
        return jsonify({'error': 'User wasnt found'})

    user.surname = params_to_edit['surname'] or user.surname
    user.name = params_to_edit['name'] or user.name
    user.position = params_to_edit['position'] or user.position
    user.age = params_to_edit['age'] or user.age
    user.speciality = params_to_edit['speciality'] or user.speciality
    user.address = params_to_edit['address'] or user.address
    user.email = params_to_edit['email'] or user.email

    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})
