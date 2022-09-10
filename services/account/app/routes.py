from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from flask_security import auth_required, hash_password, utils, login_user, login_required, logout_user, current_user

from services.account.app.models import User
from .database import db_session

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/signin')
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))
    return render_template('signin.html')


@auth.route('/signin', methods=['POST'])
def signin_post():
    is_verified = False
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if user:
        is_verified = utils.verify_password(password, user.password)
    if not is_verified:
        flash('Неверный логин или пароль')
        return redirect(url_for('auth.signin'))
    login_user(user, remember=remember)
    return redirect(url_for('auth.profile'))


@auth.route('/restore_password')
def restore_password():
    return render_template('restore_password.html')


@auth.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if current_app.security.datastore.find_user(email=email):
        flash('Пользователь уже зарегистрирован, авторизуйтесь')
        return redirect(url_for('auth.signin'))
    user = current_app.security.datastore.create_user(email=email, password=hash_password(password))
    db_session.commit()
    if user:
        flash('Создан новый пользователь, авторизуйтесь')
        return redirect(url_for('auth.signin'))
    return redirect(url_for('auth.signup'))


@auth.route('/profile')
@auth_required()
def profile():
    return render_template('profile.html')


@auth.route("/")
@auth_required()
def home():
    return redirect(url_for('auth.profile'))


@auth.route('/users')
@auth_required()
def users():
    return render_template('user_list.html')


@auth.route('/signout', methods=['GET'])
@login_required
def signout():
    logout_user()
    return redirect(url_for('auth.signin')) or request.referrer
