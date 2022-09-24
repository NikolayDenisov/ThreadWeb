from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from flask_security import auth_required, hash_password, utils, login_user, login_required, logout_user, current_user

from services.account.app.models import User
from .database import db_session
from .models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

user = Blueprint('user', __name__, url_prefix='/user')


@auth.route('/signin')
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('user.profile'))
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
    return redirect(url_for('user.profile'))


@auth.route('/restore_password')
def restore_password():
    return render_template('restore_password.html')


@auth.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('user.profile'))
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


@user.route('/profile')
@auth_required()
def profile():
    return render_template('profile.html')


@user.route("/")
@auth_required()
def home():
    return redirect(url_for('user.profile'))


@auth.route('/signout', methods=['GET'])
@login_required
def signout():
    logout_user()
    return redirect(url_for('auth.signin')) or request.referrer


@user.route('/users', methods=['GET'])
@login_required
def user_list():
    """
    limit:integer Количество элементов в ответе (по умолчанию равно 20)
    filter[email]:string	Email пользователя
    filter[groups][]: array Группы пользователя
    filter[status]: string Статус пользователя в системе.

    :return:
    """
    args = request.args
    u_limit = args.get("limit", default=20, type=None)
    u_filter = args.get("filter", default=None, type=None)
    if u_filter:
        users = User.query.filter_by().limit(u_limit)
    else:
        users = User.query.limit(u_limit)
    return render_template('user_list.html', users=users)


@user.route('/<int:user_id>', methods=['GET'])
@login_required
def select_user_by_id(user_id):
    find_user = current_app.security.datastore.find_user(id=user_id)
    if find_user:
        return render_template('profile.html', user=find_user)
    return render_template('profile.html', user=find_user)