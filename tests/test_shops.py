
import pytest
from unittest import mock
from requests.exceptions import RequestException, Timeout, ConnectionError
from app.utils.shops import ShopsInfo  # Adjust the import based on the module name where ShopsInfo is defined

class TestShopsInfo:
    # using setup and teardown method to automatically set up and clean up before and after each test.

    def setup_method(self):
        # Setup before each test method
        # A method called to prepare the test fixture before the actual test.
        self.shops = ShopsInfo(
            google_api_key="test_api_key",
            base_places_url="https://places.googleapis.com/v1/places:searchText",
        )
        # Any additional setup
        print("Setup for a test method.")

    def teardown_method(self):
        # Teardown after each test method
        # A method called after the test method to clean the environment.
        # Cleanup logic
        self.shops = None
        print("Teardown after a test method.")

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
    def mock_post_success(self, *args, **kwargs):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.successful_response
        return mock_response

    def mock_post_empty(self, *args, **kwargs):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.empty_response
        return mock_response

    def mock_post_error(self, *args, **kwargs):
        raise RequestException("API request failed")

    def mock_post_missing_data(self, *args, **kwargs):
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

    def test_get_shops_data_success(self):
        with mock.patch('requests.post', side_effect=self.mock_post_success):
            result = self.shops.get_shops_data('London')
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

    def test_get_shops_data_empty(self):
        with mock.patch('requests.post', side_effect=self.mock_post_empty):
            result = self.shops.get_shops_data('London')
            assert result == []

    def test_get_shops_data_error(self):
        with mock.patch('requests.post', side_effect=self.mock_post_error):
            result = self.shops.get_shops_data('London')
            assert result is None

    def test_get_shops_data_missing_data(self):
        with mock.patch('requests.post', side_effect=self.mock_post_missing_data):
            result = self.shops.get_shops_data('London')
            expected = [
                {
                    'name': 'N/A',
                    'address': 'Unknown Address',
                    'rating': 'N/A',
                    'google_maps_uri': 'Not available',
                    'opening_hours': 'Not available',
                    'contact_number': 'N/A',
                    'photo_url': '#'
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
    def test_map_shops_data(self, input_data, expected_output):
        result = self.shops._map_shops_data(input_data)
        assert result == expected_output

    def test_generate_photo_url(self):
        place_data_with_photo = {'photos': [{'name': 'photo_ref'}]}
        photo_url = self.shops.generate_photo_url(place_data_with_photo)
        expected_url = 'https://places.googleapis.com/v1/photo_ref/media?key=test_api_key&maxHeightPx=400&maxWidthPx=400'
        assert photo_url == expected_url

        place_data_without_photo = {}
        photo_url = self.shops.generate_photo_url(place_data_without_photo)
        assert photo_url == '#'

    def test_embed_map_url(self):
        map_url = self.shops.embed_map_url('London')
        expected_url = 'https://www.google.com/maps/embed/v1/search?key=test_api_key&q=garden+shops+in+London'
        assert map_url == expected_url

    def test_send_request_timeout(self):
        with mock.patch('requests.post', side_effect=Timeout):
            result = self.shops._send_request({}, {})
            assert result is None

    def test_send_request_connection_error(self):
        with mock.patch('requests.post', side_effect=ConnectionError):
            result = self.shops._send_request({}, {})
            assert result is None

    def test_send_request_request_exception(self):
        with mock.patch('requests.post', side_effect=RequestException):
            result = self.shops._send_request({}, {})
            assert result is None
