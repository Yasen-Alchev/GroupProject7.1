from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager    
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret!'
    app.config['SQLALCHEMY_BINDS'] = {'sample_bind': 'sqlite:///sample.db'}
    app.jinja_env.cache = {}

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app