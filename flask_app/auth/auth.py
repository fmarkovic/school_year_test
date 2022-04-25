import config
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from data_layer.models.user import User
from flask import Blueprint, render_template, request, redirect, url_for
from flask_app import db

auth = HTTPBasicAuth()
auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).one_or_none()

    if user and \
            check_password_hash(user.password, password):
        return user

@auth_bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('auth/sign_up.html')
    else:
        user = User()
        user.username = request.form["username"]  
        user.password = generate_password_hash(request.form["password"])
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('documents.index'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        pass

@auth_bp.errorhandler(404)
def page_not_found(e):
    return render_template('auth/404.html')