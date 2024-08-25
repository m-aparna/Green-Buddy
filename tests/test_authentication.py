from app.models import User
from .conftest import mock_sign_up_data, mock_login_data

# Test case for sign up - properly commiting new user to DB
def test_signup(client, app):
    response = client.post("/sign-up", data=mock_sign_up_data)

    with app.app_context():
        # Assert status code
        assert response.status_code == 302 # As redirect to homepage should happen on success
        # Check number of users
        assert User.query.count() == 1
        # Check email
        assert User.query.first().email == mock_sign_up_data["email"]
        #Check username
        assert User.query.first().username == mock_sign_up_data["username"]

# Check if sign up redirects properly
def test_sign_up_redirection(client):
    response = client.post("/sign-up", data=mock_sign_up_data)

    assert response.status_code == 302

    # Get the redirect URL from the Location header
    redirect_location = response.headers.get('Location')
    assert redirect_location == "/"

# Check if login redirects properly
def test_login_redirection(client):
    client.post("/sign-up", data=mock_sign_up_data)
    response = client.post("/login", data=mock_login_data)

    assert response.status_code == 302

    # Get the redirect URL from the Location header
    redirect_location = response.headers.get('Location')
    assert redirect_location == "/"

# Check invalid login without sign up first
def test_invalid_login(client):
    response_login = client.post("/login", data=mock_login_data)

    assert response_login.status_code == 401 # Since it returns 401 code

# Check logout
def test_logout(client):
    client.post("/sign-up", data=mock_sign_up_data)
    client.post("/login", data=mock_login_data)

    response = client.get("/logout")
    assert response.status_code == 302

    redirect_location = response.headers.get('Location')
    assert redirect_location == "/"
