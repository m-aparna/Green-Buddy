import pytest
from unittest import mock
from requests.exceptions import RequestException
from app.utils.weather import WeatherInfo
from app.utils.planting_advice import PlantingAdvice

class TestWeatherInfo:
    # using setup and teardown method to automatically set up and clean up before and after each test.

    def setup_method(self):
        # Setup before each test method
        self.weather_info = WeatherInfo()
        self.planting = PlantingAdvice()
        print("Setup for a test method.......")

    def teardown_method(self):
        # Teardown after each test method
        self.weather_info = None
        self.planting = None
        print("Teardown.....")

    # Mock responses for various scenarios
    successful_weather_response = {
        'list': [
            {
                'dt_txt': '2024-08-21 12:00:00',
                'main': {'temp': 22, 'pressure': 1012, 'humidity': 65},
                'weather': [{'description': 'clear sky', 'icon': '01d'}],
                'sys': {'pod': 'd'},
                'wind': {'speed': 5.0}
            }
        ]
    }

    empty_weather_response = {'list': []}

    invalid_weather_response = {'wrong_key': 'invalid structure'}

    error_response = {}  # Simulating an error response

    # Mock request functions
    def mock_get_success(self, *args, **kwargs):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.successful_weather_response
        return mock_response

    def mock_get_empty(self, *args, **kwargs):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.empty_weather_response
        return mock_response

    def mock_get_invalid(self, *args, **kwargs):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.invalid_weather_response
        return mock_response

    def mock_get_error(self, *args, **kwargs):
        raise RequestException("API request failed")

    def test_get_weather_data_success(self):
        with mock.patch('requests.get', side_effect=self.mock_get_success):
            result = self.weather_info.get_weather_data('London')
            expected = self.successful_weather_response
            assert result == expected

    def test_get_weather_data_empty(self):
        with mock.patch('requests.get', side_effect=self.mock_get_empty):
            result = self.weather_info.get_weather_data('London')
            assert result == self.empty_weather_response

    def test_get_weather_data_error(self):
        with mock.patch('requests.get', side_effect=self.mock_get_error):
            result = self.weather_info.get_weather_data('London')
            assert result is None

    def test_process_weather_data_success(self):
        with mock.patch('requests.get', side_effect=self.mock_get_success):
            weather_data = self.weather_info.get_weather_data('London')
            result = self.weather_info.process_weather_data(weather_data)
            expected = [
                {
                    'date': '2024-08-21',
                    'temperature': 22,
                    'pressure': 1012.00,
                    'humidity': 65.00,
                    'wind_speed': 5.00,
                    'weather': 'clear sky',
                    'icon': '01d'
                }
            ]
            assert result == expected

    def test_process_weather_data_empty(self):
        with mock.patch('requests.get', side_effect=self.mock_get_empty):
            weather_data = self.weather_info.get_weather_data('London')
            result = self.weather_info.process_weather_data(weather_data)
            assert result == []

    def test_process_weather_data_invalid(self):
        with mock.patch('requests.get', side_effect=self.mock_get_invalid):
            weather_data = self.weather_info.get_weather_data('London')
            result = self.weather_info.process_weather_data(weather_data)
            assert result == []

    def test_check_for_bad_weather_success(self):
        with mock.patch('requests.get', side_effect=self.mock_get_success):
            weather_data = self.weather_info.get_weather_data('London')
            processed_data = self.weather_info.process_weather_data(weather_data)
            result = self.weather_info.check_for_bad_weather(processed_data)
            expected = []  # Update with expected bad weather alerts if any
            assert result == expected

    def test_provide_planting_advice_success(self):
        with mock.patch('requests.get', side_effect=self.mock_get_success):
            weather_data = self.weather_info.get_weather_data('London')
            processed_data = self.weather_info.process_weather_data(weather_data)
            result = self.planting.provide_planting_advice(processed_data)
            expected = [
                {
                    'date': '2024-08-21',
                    'advice': 'Good weather for planting during the Vegetative phase. Consider planting tomatoes or basil.',
                    'phase': 'Vegetative phase',
                    'plant_suggestion': 'tomatoes or basil'
                }
            ]  # Update with expected planting advice
            assert result == expected

    @pytest.mark.parametrize("input_data, expected_output", [
        (successful_weather_response, [
            {
                'date': '2024-08-21',
                'temperature': 22,
                'pressure': 1012.00,
                'humidity': 65.00,
                'wind_speed': 5.00,
                'weather': 'clear sky',
                'icon': '01d'
            }
        ]),
        (empty_weather_response, []),
        (invalid_weather_response, []),
    ])
    def test_map_weather_data_sucess(self, input_data, expected_output):
        # Test the mapping of weather data from the API response to the expected format.
        if input_data == self.successful_weather_response:
            result = self.weather_info.process_weather_data(input_data)
        else:
            result = self.weather_info.process_weather_data({'list': input_data})
        assert result == expected_output
