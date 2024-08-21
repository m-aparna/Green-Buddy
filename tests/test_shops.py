import pytest
from unittest import mock
from requests.exceptions import RequestException, Timeout, ConnectionError
from app.shops import ShopsInfo  # Adjust the import based on the module name where ShopsInfo is defined


@pytest.fixture
# Fixtures to create an instance of ShopsInfo with api keys and Urls.
def shops():
    return ShopsInfo(
        places_api_key="test_api_key",
        base_places_url="https://places.googleapis.com/v1/places:searchText",
        google_maps_api_key="test_google_maps_key"
    )


#  Here we are mocking the API responses
successful_response = {
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

empty_response = {'places': []}

error_response = None  # failed response


# Mock post request functions
def mock_post_success(*args, **kwargs):
    # Creates a fake requests response object
    mock_response = mock.Mock()
    # Mock the status code
    mock_response.status_code = 200
    # Mock the json method to return shops data
    mock_response.json.return_value = successful_response
    return mock_response


def mock_post_empty(*args, **kwargs):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = empty_response
    return mock_response


def mock_post_error(*args, **kwargs):
    raise RequestException("API request failed")


def mock_post_missing_data(*args, **kwargs):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    # Missing 'all keys except address
    mock_response.json.return_value = {
        'places': [
            {
                'formattedAddress': 'Unknown Address',
                # Missing all other fields
            }
        ]
    }
    return mock_response


def test_get_shops_data_success(shops):
    # Test that get_shops_data successfully fetches and maps shop data.
    with mock.patch('requests.post', side_effect=mock_post_success):
        result = shops.get_shops_data('London')
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


def test_get_shops_data_empty(shops):
    # Test that get_shops_data handles an empty response correctly.
    with mock.patch('requests.post', side_effect=mock_post_empty):
        result = shops.get_shops_data('London')
        assert result == []


def test_get_shops_data_error(shops):
    # Test that get_shops_data handles a request exception properly.
    with mock.patch('requests.post', side_effect=mock_post_error):
        result = shops.get_shops_data('London')
        assert result is None


def test_get_shops_data_missing_data(shops):
    # Test that get_shops_data handles a response with missing keys correctly.
    with mock.patch('requests.post', side_effect=mock_post_missing_data):
        result = shops.get_shops_data('London')
        expected = [
            {
                'name': 'N/A',  # Default value when 'displayName' is missing
                'address': 'Unknown Address',
                'rating': 'N/A',  # Default value when 'rating' is missing
                'google_maps_uri': 'Not available',   # Default value when 'googleMapsUri' is missing
                'opening_hours': 'Not available',     # Default value when 'currentOpeningHours' is missing
                'contact_number': 'N/A',              # Default value when 'nationalPhoneNumber' is missing
                'photo_url': '#'                      # Default value when 'photos' is missing
            }
        ]
        assert result == expected


@pytest.mark.parametrize("input_data, expected_output", [
    (successful_response, [
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
    (empty_response, []),
    (error_response, [])
])
# Test the mapping of shop data from the API response to the expected format.
def test_map_shops_data(shops, input_data, expected_output):
    result = shops._map_shops_data(input_data)
    assert result == expected_output


# Test that generate_photo_url correctly creates a photo URL or returns a default value.
def test_generate_photo_url(shops):
    place_data_with_photo = {'photos': [{'name': 'photo_ref'}]}
    photo_url = shops.generate_photo_url(place_data_with_photo)
    expected_url = 'https://places.googleapis.com/v1/photo_ref/media?key=test_api_key&maxHeightPx=400&maxWidthPx=400'
    assert photo_url == expected_url

    place_data_without_photo = {}
    photo_url = shops.generate_photo_url(place_data_without_photo)
    assert photo_url == '#'


# Test that embed_map_url generates the correct Google Maps embed URL.
def test_embed_map_url(shops):
    map_url = shops.embed_map_url('London')
    expected_url = 'https://www.google.com/maps/embed/v1/search?key=test_google_maps_key&q=garden+shops+in+London'
    assert map_url == expected_url


# Test that _send_request handles a Timeout exception properly."
def test_send_request_timeout(shops):
    with mock.patch('requests.post', side_effect=Timeout):
        result = shops._send_request({}, {})
        assert result is None


# Test that _send_request handles a ConnectionError exception properly.
def test_send_request_connection_error(shops):
    with mock.patch('requests.post', side_effect=ConnectionError):
        result = shops._send_request({}, {})
        assert result is None


# Test that _send_request handles a general RequestException properly.
def test_send_request_request_exception(shops):
    with mock.patch('requests.post', side_effect=RequestException):
        result = shops._send_request({}, {})
        assert result is None
