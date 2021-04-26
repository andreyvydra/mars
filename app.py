import os

from flask import Flask, render_template, request, make_response, session, jsonify
from requests import get
from werkzeug.exceptions import abort
from geocoder import *

import jobs_resources
from data.departments import Departments
from data.jobs import Jobs
from data.users import User
from data import db_session, user_api
from forms import RegisterForm, LoginForm, JobsForm, DepartmentsForm
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask_restful import reqparse, abort, Api, Resource
import user_resources

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("list_of_jobs.html", jobs=jobs)


@app.route("/departments")
def departments():
    db_sess = db_session.create_session()
    deps = db_sess.query(Departments).all()
    return render_template("list_of_departments.html", departments=deps)


@app.route("/department", methods=['POST', 'GET'])
def department():
    form = DepartmentsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = Departments(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data,
            user_id=current_user.id
        )
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/departments')
    return render_template('department.html', title='Добавление департамента',
                           form=form)


@app.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id == 1:
            dep = db_sess.query(Departments).filter(Departments.id == id).first()
        else:
            dep = db_sess.query(Departments).filter(Departments.id == id,
                                                    current_user.id == Departments.user_id).first()
        if dep:
            form.title.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            dep = db_sess.query(Departments).filter(Departments.id == id).first()
        else:
            dep = db_sess.query(Departments).filter(Departments.id == id,
                                                    current_user.id == Departments.user_id).first()
        if dep:
            dep.title = form.title.data
            dep.chief = form.chief.data
            dep.members = form.members.data
            dep.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('department.html',
                           title='Редактирование департамента',
                           form=form
                           )


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Departments).filter(Departments.id == id,
                                            Departments.user_id == current_user.id
                                            ).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            speciality=form.speciality.data,
            position=form.position.data,
            email=form.email_or_login.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/job', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(job=form.title.data, team_leader=form.team_leader.data,
                   work_size=form.work_size.data,
                   collaborators=form.collaborators.data,
                   is_finished=form.is_finished.data,
                   user_id=current_user.id)
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('job.html', title='Добавление работы',
                           form=form)


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id == 1:
            job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        else:
            job = db_sess.query(Jobs).filter(Jobs.id == id, current_user.id == Jobs.user_id).first()
        if job:
            form.title.data = job.job
            form.team_leader.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        else:
            job = db_sess.query(Jobs).filter(Jobs.id == id, current_user.id == Jobs.user_id).first()
        if job:
            job.job = form.title.data
            job.team_leader = form.team_leader.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('job.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter(Jobs.id == id,
                                      Jobs.user_id == current_user.id
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    response_json = get(f'http://127.0.0.1:8000/api/users/{user_id}').json()

    if 'error' in response_json:
        return jsonify(response_json)
    user = response_json['user']
    if 'address' in user:
        address = user['address']
    else:
        address = 'Москва'
        user['address'] = address

    toponym_longitude, toponym_lattitude = get_coordinates(address)
    ll = ",".join([str(toponym_longitude), str(toponym_lattitude)])

    save_map(ll, '0.06,0.06', l='sat')

    user['city'] = get_city(address)

    return render_template('users_show.html',
                           user=user
                           )


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    api.add_resource(user_resources.UserResource, '/api/v2/users/<int:user_id>')
    api.add_resource(user_resources.UserListResource, '/api/v2/users/')
    api.add_resource(jobs_resources.JobsListResource, '/api/v2/jobs/')
    api.add_resource(jobs_resources.JobsResource, '/api/v2/jobs/<int:jobs_id>')
    app.register_blueprint(user_api.blueprint)
    app.run(host='127.0.0.1', port=8000)
