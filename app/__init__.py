from flask import Flask
from config import secret_key


# Function to initialize flask app
def flask_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key


    # Import blueprints 
    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    return app


