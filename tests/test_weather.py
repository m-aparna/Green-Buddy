import pytest
from unittest import mock
from requests.exceptions import RequestException
from app.utils.weather import WeatherInfo
from app.utils.planting_advice import PlantingAdvice

@pytest.fixture
def weather_info():
    return WeatherInfo()

@pytest.fixture
def planting():
    return PlantingAdvice()

class TestWeatherInfo:
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

    invalid_weather_response = {'wrong_key': 'unexpected structure'}

    # Mock request functions

    def mock_get_success(*args, **kwargs):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = TestWeatherInfo.successful_weather_response
        return mock_response


    def mock_get_empty(*args, **kwargs):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = TestWeatherInfo.empty_weather_response
        return mock_response


    def mock_get_invalid(*args, **kwargs):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = TestWeatherInfo.invalid_weather_response
        return mock_response


    def mock_get_error(*args, **kwargs):
        raise RequestException("API request failed")

    def test_get_weather_data_success(self, weather_info):
        with mock.patch('requests.get', side_effect=self.mock_get_success):
            result = weather_info.get_weather_data('London')
            assert result == self.successful_weather_response

    def test_get_weather_data_empty(self, weather_info):
        with mock.patch('requests.get', side_effect=self.mock_get_empty):
            result = weather_info.get_weather_data('London')
            assert result == self.empty_weather_response

    def test_get_weather_data_error(self, weather_info):
        with mock.patch('requests.get', side_effect=self.mock_get_error):
            result = weather_info.get_weather_data('London')
            assert result is None

    def test_process_weather_data_success(self, weather_info):
        with mock.patch('requests.get', side_effect=self.mock_get_success):
            weather_data = weather_info.get_weather_data('London')
            result = weather_info.process_weather_data(weather_data)
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

    def test_process_weather_data_empty(self, weather_info):
        with mock.patch('requests.get', side_effect=self.mock_get_empty):
            weather_data = weather_info.get_weather_data('London')
            result = weather_info.process_weather_data(weather_data)
            assert result == []

    def test_process_weather_data_invalid(self, weather_info):
        with mock.patch('requests.get', side_effect=self.mock_get_invalid):
            weather_data = weather_info.get_weather_data('London')
            result = weather_info.process_weather_data(weather_data)
            assert result == []

    def test_check_for_bad_weather_success(self, weather_info):
        with mock.patch('requests.get', side_effect=self.mock_get_success):
            weather_data = weather_info.get_weather_data('London')
            processed_data = weather_info.process_weather_data(weather_data)
            result = weather_info.check_for_bad_weather(processed_data)
            expected = []  # Update with expected bad weather alerts if any
            assert result == expected

    def test_provide_planting_advice_success(self, weather_info, planting):
        with mock.patch('requests.get', side_effect=self.mock_get_success):
            weather_data = weather_info.get_weather_data('London')
            processed_data = weather_info.process_weather_data(weather_data)
            result = planting.provide_planting_advice(processed_data)
            expected = [
                {
                    'date': '2024-08-21',
                    'advice': 'Good weather for planting during the Vegetative phase. Consider planting tomatoes or basil.',
                    'phase': 'Vegetative phase',
                    'plant_suggestion': 'tomatoes or basil'
                }
            ]
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
    def test_map_weather_data_success(self, weather_info, input_data, expected_output):
        if 'list' in input_data:
            result = weather_info.process_weather_data(input_data)
        else:
            result = weather_info.process_weather_data({'list': input_data})
        assert result == expected_output

if __name__ == "__main__":
    pytest.main()
