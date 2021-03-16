from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.users import User


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        jobs = session.query(User).get(user_id)
        return jsonify({'user': jobs.to_dict(
            only=('id',
                  'surname',
                  'name',
                  'age',
                  'position',
                  'speciality',
                  'address',
                  'email'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id',
                  'surname',
                  'name',
                  'age',
                  'position',
                  'speciality',
                  'address',
                  'email')) for item in users]})

    def post(self):
        args = parser.parse_args()
        abort_if_email_found(args['email'])
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


def abort_if_email_found(email):
    session = db_session.create_session()
    user = session.query(User).get(email)
    if user:
        abort(404, message=f"Email was found")


parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str)
parser.add_argument('surname', required=True, type=str)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True, type=str)
parser.add_argument('speciality', required=True, type=str)
parser.add_argument('address', required=True, type=str)
parser.add_argument('email', required=True, type=str)
