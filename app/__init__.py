from flask import Flask
from config import secret_key
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Create db object
db = SQLAlchemy()
db_name = 'User.db'


# Function to initialize flask app
def flask_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'

    # Initialise db
    db.init_app(app)

    # Import blueprints 
    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    # Create db
    with app.app_context():
        db.create_all()
        print("DB created!")

    # Set up login manager
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'

    # Load the correct user using their id
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
