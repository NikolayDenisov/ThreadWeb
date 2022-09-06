from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_security import auth_required, hash_password, utils, login_user, login_required, logout_user
from models import User
from . import app

auth = Blueprint('auth', __name__)


@auth.route('/signin')
def signin():
    return render_template('signin.html')


@auth.route('/signin', methods=['POST'])
def signin_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if not user and not utils.verify_password(password, user.password):
        flash('Неверный логин или пароль')
        return redirect(url_for('auth.signin'))
    login_user(user, remember=remember)
    return redirect(url_for('auth.profile'))


@auth.route('/restore_password')
def restore_password():
    return render_template('restore_password.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if not app.security.datastore.find_user(email=email):
        flash('Пользователь уже зарегистрирован, авторизуйтесь')
        return redirect(url_for('auth.signin'))
    # db.create_user(email=email, password=hash_password(password))
    print(request.form, hash_password(password))
    # return redirect(url_for('account.main'))


@auth.route('/profile')
@auth_required()
def profile():
    return render_template('profile.html')


@auth.route("/")
@auth_required()
def home():
    return redirect(url_for('auth.profile'))


@auth.route('/signout', methods=['GET'])
@login_required
def signout():
    logout_user()
    return redirect(url_for('auth.signin')) or request.referrer
