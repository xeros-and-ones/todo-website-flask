from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
site_db = 'siteDB.db'


class Config(object):
    SECRET_KEY = 'momomomo'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{site_db}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app


def create_database(app):
    if not path.exists('website/' + site_db):
        db.create_all(app=app)
        print('created database')
