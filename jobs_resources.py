from datetime import datetime

from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.jobs import Jobs


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_job_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify({'jobs': jobs.to_dict(
            only=('id',
                  'job',
                  'team_leader',
                  'work_size',
                  'collaborators',
                  'is_finished',
                  'start_date',
                  'end_date',
                  'user.id'))})

    def delete(self, jobs_id):
        abort_if_job_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('id',
                  'job',
                  'team_leader',
                  'work_size',
                  'collaborators',
                  'is_finished',
                  'start_date',
                  'end_date',
                  'user.id')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            job=args['job'],
            team_leader=args['team_leader'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished'],
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(job_id)
    if not jobs:
        abort(404, message=f"Job {job_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('job', required=True, type=str)
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True, type=str)
parser.add_argument('is_finished', required=True, type=bool)
