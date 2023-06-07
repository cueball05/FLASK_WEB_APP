from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from os import path
from flask_login import LoginManager

# creates object instance of SQLALchemy
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'  # in production never expose this secret key get it hashed or encrypted and imported somewhere
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # import the views and auth Blueprints
    from .views import views
    from .auth import auth

    # and register them
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # import the classes User and Note from models source: https://flask.palletsprojects.com/en/2.3.x/blueprints/
    from .models import User, Note

    login_manager = LoginManager()
    # redirects the user to the login view if the user needs to login
    login_manager.login_view='auth.login'
    # configure the login as below
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        db.create_all()

    return app