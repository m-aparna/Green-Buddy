# Contains the main fixtures
import pytest
from app import create_app, db

# Set up mock data
mock_sign_up_data = {
    "email": "test@test.com",
    "username": "Test User",
    "password1": "testpassword",
    "password2": "testpassword"
}

mock_login_data = {
    "email": "test@test.com",
    "password": "testpassword"
}

mock_plant_data = {
    "plant_name": "Mintu",
    "plant_species": "Baby Sun Rose",
    "details": "This is my first plant. Water every 3 days. Fertilize twice every month",
    "user_id": 1
}

# Fixture to create flask app
@pytest.fixture()
def app():
    app = create_app('sqlite:///:memory:')

    # Create the db
    with app.app_context():
        db.create_all() 
        yield app  
        db.drop_all()  

# Fixture to create client
@pytest.fixture()
def client(app):
    return app.test_client() # Function is inside the tests
