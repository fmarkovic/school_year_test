# Imports Required Use Pip for there dependencies
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    
    from flask_app.auth import login_manager
    login_manager.init_app(app)

    from flask_app.auth import auth_bp
    from flask_app.documents import documents_bp
    from flask_app.invites import invites_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(documents_bp, url_prefix="/documents")
    app.register_blueprint(invites_bp, url_prefix="/invites")

    return app
