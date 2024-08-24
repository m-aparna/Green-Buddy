import pytest
from unittest import mock
from requests.exceptions import RequestException, Timeout, ConnectionError
from app.utils.shops import ShopsInfo  # Adjust the import based on the module name where ShopsInfo is defined

# Define fixtures
@pytest.fixture
def shops_info():
    """Fixture to create and provide an instance of ShopsInfo"""
    return ShopsInfo(
        google_api_key="test_api_key",
        base_places_url="https://places.googleapis.com/v1/places:searchText",
    )

# Mock response functions
def mock_post_success_function(*args, **kwargs):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'places': [
            {
                'displayName': {'text': 'Camden Garden Centre'},
                'formattedAddress': '2 Barker Dr, London NW1 0JW, UK',
                'rating': 4.2,
                'googleMapsUri': 'https://maps.google.com/?cid=18368197700183042617',
                'currentOpeningHours': {
                    'weekdayDescriptions': ['Mon-Fri: 9am-5pm', 'Sat: 10am-4pm']
                },
                'nationalPhoneNumber': '020 7387 7080',
                'photos': [{'name': 'photo_ref'}]
            }
        ]
    }
    return mock_response

def mock_post_empty_function(*args, **kwargs):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'places': []}
    return mock_response

def mock_post_missing_data_function(*args, **kwargs):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'places': [
            {
                'formattedAddress': 'Unknown Address',
            }
        ]
    }
    return mock_response

@pytest.fixture
def mock_post_success(shops_info):
    """Fixture to mock a successful post request"""
    with mock.patch('requests.post', side_effect=mock_post_success_function):
        yield

@pytest.fixture
def mock_post_empty(shops_info):
    """Fixture to mock an empty post request response"""
    with mock.patch('requests.post', side_effect=mock_post_empty_function):
        yield

@pytest.fixture
def mock_post_error(shops_info):
    """Fixture to mock an error during post request"""
    with mock.patch('requests.post', side_effect=RequestException("API request failed")):
        yield

@pytest.fixture
def mock_post_missing_data(shops_info):
    """Fixture to mock a post request with missing data"""
    with mock.patch('requests.post', side_effect=mock_post_missing_data_function):
        yield

# Define the test class
class TestShopsInfo:

    def test_get_shops_data_success(self, shops_info, mock_post_success):
        result = shops_info.get_shops_data('London')
        expected = [
            {
                'name': 'Camden Garden Centre',
                'address': '2 Barker Dr, London NW1 0JW, UK',
                'rating': 4.2,
                'google_maps_uri': 'https://maps.google.com/?cid=18368197700183042617',
                'opening_hours': 'Mon-Fri: 9am-5pm\nSat: 10am-4pm',
                'contact_number': '020 7387 7080',
                'photo_url': 'https://places.googleapis.com/v1/photo_ref/media?key=test_api_key&maxHeightPx=400&maxWidthPx=400'
            }
        ]
        assert result == expected

    @pytest.mark.parametrize("mock_function, expected_output", [
        (mock_post_success_function, [
            {
                'name': 'Camden Garden Centre',
                'address': '2 Barker Dr, London NW1 0JW, UK',
                'rating': 4.2,
                'google_maps_uri': 'https://maps.google.com/?cid=18368197700183042617',
                'opening_hours': 'Mon-Fri: 9am-5pm\nSat: 10am-4pm',
                'contact_number': '020 7387 7080',
                'photo_url': 'https://places.googleapis.com/v1/photo_ref/media?key=test_api_key&maxHeightPx=400&maxWidthPx=400'
            }
        ]),
        (mock_post_empty_function, []),
        (mock_post_missing_data_function, [
            {
                'name': 'N/A',
                'address': 'Unknown Address',
                'rating': 'N/A',
                'google_maps_uri': 'Not available',
                'opening_hours': 'Not available',
                'contact_number': 'N/A',
                'photo_url': '#'
            }
        ])
    ])
    def test_map_shops_data(self, shops_info, mock_function, expected_output):
        with mock.patch('requests.post', side_effect=mock_function):
            input_data = shops_info._send_request({}, {})
            result = shops_info._map_shops_data(input_data)
            assert result == expected_output

    def test_generate_photo_url(self, shops_info):
        place_data_with_photo = {'photos': [{'name': 'photo_ref'}]}
        photo_url = shops_info.generate_photo_url(place_data_with_photo)
        expected_url = 'https://places.googleapis.com/v1/photo_ref/media?key=test_api_key&maxHeightPx=400&maxWidthPx=400'
        assert photo_url == expected_url

        place_data_without_photo = {}
        photo_url = shops_info.generate_photo_url(place_data_without_photo)
        assert photo_url == '#'

    def test_embed_map_url(self, shops_info):
        map_url = shops_info.embed_map_url('London')
        expected_url = 'https://www.google.com/maps/embed/v1/search?key=test_api_key&q=garden+shops+in+London'
        assert map_url == expected_url

    def test_send_request_timeout(self, shops_info):
        with mock.patch('requests.post', side_effect=Timeout):
            result = shops_info._send_request({}, {})
            assert result is None

    def test_send_request_connection_error(self, shops_info):
        with mock.patch('requests.post', side_effect=ConnectionError):
            result = shops_info._send_request({}, {})
            assert result is None

    def test_send_request_request_exception(self, shops_info):
        with mock.patch('requests.post', side_effect=RequestException):
            result = shops_info._send_request({}, {})
            assert result is None

    @pytest.mark.parametrize("location, expected_result", [
        ("London", True),
        ("New York", True),
        ("", False),
        (None, False),
        ("1234", False),
        ("@London#", False)
    ])
    def test_is_valid_location(self, shops_info, location, expected_result):
        result = shops_info.is_valid_location(location)
        assert result == expected_result
