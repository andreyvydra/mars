import flask
from flask import jsonify, request

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id',
                                    'team_leader',
                                    'job',
                                    'work_size',
                                    'collaborators',
                                    'start_date',
                                    'end_date',
                                    'is_finished'
                                    )) for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_jobs(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('id',
                                       'team_leader',
                                       'job',
                                       'work_size',
                                       'collaborators',
                                       'start_date',
                                       'end_date',
                                       'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id',
                  'job',
                  'team_leader',
                  'work_size',
                  'collaborators',
                  'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(int(request.json['id']))
    print(job)
    if job:
        return jsonify({'error': 'Id already exists'})
    job = Jobs(
        id=request.json['id'],
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/', methods=['PUT'])
def update_job():
    params_to_edit = {
        'id': None,
        'job': None,
        'team_leader': None,
        'work_size': None,
        'collaborators': None,
        'is_finished': None
    }
    print(request.json)
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in params_to_edit.keys() for key in request.json):
        return jsonify({'error': 'Bad request'})
    else:
        for key in request.json:
            params_to_edit[key] = request.json[key]

    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(int(request.json['id']))

    job.job = params_to_edit['job'] if params_to_edit['job'] is not None else job.job
    job.team_leader = params_to_edit['team_leader'] if params_to_edit['team_leader'] is not None else job.team_leader
    job.work_size = params_to_edit['work_size'] if params_to_edit['work_size'] is not None else job.work_size
    job.collaborators = params_to_edit['collaborators'] if params_to_edit[
                                                               'collaborators'] is not None else job.collaborators
    job.is_finished = params_to_edit['is_finished'] if params_to_edit['is_finished'] is not None else job.is_finished

    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})
