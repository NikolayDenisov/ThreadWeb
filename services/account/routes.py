from flask import Blueprint, render_template, request, redirect, flash, url_for
# from .db import User
import uuid as uuid_pkg
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    # user = User.query.filter_by(email=email).first()
    # if not user and not check_password_hash(user.password, password):
    #     flash('Неверный логин или пароль')
    #     return redirect(url_for('auth.login'))
    # login_user(user, remember=remember)
    return redirect(url_for('auth.login'))


@auth.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')


@auth.route('/register')
def register():
    return render_template('register.html')
