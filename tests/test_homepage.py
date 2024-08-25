# Test Homepage
def test_home(client):
    response = client.get("/")

    # Check status code
    assert response.status_code == 200

    # Check title
    expected_title = b"<title>Green Buddy</title>"
    assert expected_title in response.data

    # Check any heading
    expected_heading = b"<h1>Welcome to Green Buddy</h1>"
    assert expected_heading in response.data
