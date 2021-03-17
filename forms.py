from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email_or_login = EmailField('Почта / Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    speciality = StringField('Специальность', validators=[DataRequired()])
    address = TextAreaField('Адрес')
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class JobsForm(FlaskForm):
    title = StringField('Заголовок работы', validators=[DataRequired()])
    team_leader = StringField('ID Руководителя команды', validators=[DataRequired()])
    work_size = StringField('Время работы (в часах)', validators=[DataRequired()])
    collaborators = StringField('Соучастники', validators=[DataRequired()])
    is_finished = BooleanField('Работа завершена?')
    submit = SubmitField('Применить')


class DepartmentsForm(FlaskForm):
    title = StringField('Название департамента', validators=[DataRequired()])
    chief = StringField('ID Руководителя', validators=[DataRequired()])
    members = StringField('Члены департамента', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Применить')
