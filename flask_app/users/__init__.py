from flask import Blueprint

user_bp = Blueprint('user', __name__, template_folder='templates')
#from flask_restx import Namespace

#users_api = Namespace('users',
#                      description='User related operations')

#from .apis import UsersApi, UsersImageUploadApi, UsersSendNotificationApi
