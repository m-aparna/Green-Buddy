import pytest
from unittest import mock
from requests.exceptions import RequestException, Timeout, ConnectionError
from app.utils.shops import ShopsInfo
"""Fixtures are functions, which will run before each test function to which it is applied. Fixtures are used to feed 
some data to the tests such as database connections, URLs to test and some sort of input data.instead of running the 
same code for every test, we can attach fixture function to the tests and it will run and return the data to the test 
before executing each test."""

# Fixtures to create an instance of ShopsInfo with api keys and Urls.
@pytest.fixture
def shops():
    return ShopsInfo(
        google_api_key="test_api_key",
        base_places_url="https://places.googleapis.com/v1/places:searchText",
    )

class TestShopsInfo:
    # Mock responses for various tests
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

    error_response = None  # Simulating a failed response


    def mock_post_success(*args, **kwargs):
        # Creates a fake requests response object
        mock_response = mock.Mock()
        # Mock the status code
        mock_response.status_code = 200
        # Mock the json method to return shops data
        mock_response.json.return_value = TestShopsInfo.successful_response
        return mock_response


    def mock_post_empty(*args, **kwargs):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = TestShopsInfo.empty_response
        return mock_response


    def mock_post_error(*args, **kwargs):
        raise RequestException("API request failed")

    # Mock response when there is missing data
    def mock_post_missing_data(*args, **kwargs):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'places': [
                {
                    'formattedAddress': 'Unknown Address',
                    # Missing all other fields
                }
            ]
        }
        return mock_response

    """mock.patch is a function from unittest.mock library that allows to replace an object or method with a mock object(e.g.request.post)"""
    """side_effect is an attribute of a mock  that is useful for raising  exceptions when the mock is called and simulate dynamic responses(e.g. self.mock_post_success simulates a successful api response . """

    def test_get_shops_data_success(self, shops):
        # Test that get_shops_data successfully fetches and maps shop data.
        with mock.patch('requests.post', side_effect=self.mock_post_success):
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

    def test_get_shops_data_empty(self, shops):
        # Test to check get_shops_data handles empty data
        with mock.patch('requests.post', side_effect=self.mock_post_empty):
            result = shops.get_shops_data('London')
            assert result == []

    def test_get_shops_data_error(self, shops):
        # Test to check get_shops_data handles errors or exceptions
        with mock.patch('requests.post', side_effect=self.mock_post_error):
            result = shops.get_shops_data('London')
            assert result is None

    def test_get_shops_data_missing_data(self, shops):
        # Test that get_shops_data handles a response with missing keys correctly.
        with mock.patch('requests.post', side_effect=self.mock_post_missing_data):
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

    #  builtin decorator to enable parametrization of arguments for a test function.
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
    def test_map_shops_data(self, shops, input_data, expected_output):
        result = shops._map_shops_data(input_data)
        assert result == expected_output

    # Test that generate_photo_url correctly creates a photo URL or returns a default value if photo url is not present.

    def test_generate_photo_url(self, shops):
        place_data_with_photo = {'photos': [{'name': 'photo_ref'}]}
        photo_url = shops.generate_photo_url(place_data_with_photo)
        expected_url = 'https://places.googleapis.com/v1/photo_ref/media?key=test_api_key&maxHeightPx=400&maxWidthPx=400'
        assert photo_url == expected_url

        place_data_without_photo = {}
        photo_url = shops.generate_photo_url(place_data_without_photo)
        assert photo_url == '#'

    # Test that embed_map_url generates the correct Google Maps embed URL.
    def test_embed_map_url(self, shops):
        map_url = shops.embed_map_url('London')
        expected_url = 'https://www.google.com/maps/embed/v1/search?key=test_api_key&q=garden+shops+in+London'
        assert map_url == expected_url
    # Test  to check  send_request function handles timeout error
    def test_send_request_timeout(self, shops):
        with mock.patch('requests.post', side_effect=Timeout):
            result = shops._send_request({}, {})
            assert result is None
    # connection error
    def test_send_request_connection_error(self, shops):
        with mock.patch('requests.post', side_effect=ConnectionError):
            result = shops._send_request({}, {})
            assert result is None
    # Test to check send request handles Requestexception
    def test_send_request_request_exception(self, shops):
        with mock.patch('requests.post', side_effect=RequestException):
            result = shops._send_request({}, {})
            assert result is None

    @pytest.mark.parametrize("location, expected_result", [
        ("London", True),  # Valid city name should return true
        ("New York", True),
        ("", False),
        ("1234", False),
        ("@London#", False)  # Special characters should result in false
    ])
    # Test to check if is_valid_location handles proper location inputs
    def test_is_valid_location(self, shops, location, expected_result):
        result = shops.is_valid_location(location)
        assert result == expected_result
