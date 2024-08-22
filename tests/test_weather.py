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

# Mock responses for various scenarios
successful_weather_response = {
    'list': [
        {
            'dt_txt': '2024-08-21 12:00:00',
            'main': {'temp': 22, 'pressure': 1012, 'humidity': 65},
            'weather': [{'description': 'clear sky', 'icon': '01d'}],
            'sys': {'pod': 'd'},
            'wind': {'speed': 5.0}
        },
        # Add more mock data to cover other scenarios
    ]
}

empty_weather_response = {'list': []}

malformed_weather_response = {'wrong_key': 'unexpected structure'}

error_response = {}  # Simulating an error response

# Mock request functions
def mock_get_success(*args, **kwargs):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = successful_weather_response
    return mock_response

def mock_get_empty(*args, **kwargs):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = empty_weather_response
    return mock_response

def mock_get_malformed(*args, **kwargs):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = malformed_weather_response
    return mock_response

def mock_get_error(*args, **kwargs):
    raise RequestException("API request failed")



def test_get_weather_data_success(weather_info):
    # Test that get_weather_data fetches weather data successfully.
    with mock.patch('requests.get', side_effect=mock_get_success):
        result = weather_info.get_weather_data('London')
        expected = successful_weather_response
        assert result == expected


def test_get_weather_data_empty(weather_info):
    # Test that get_weather_data handles an empty response correctly.
    with mock.patch('requests.get', side_effect=mock_get_empty):
        result = weather_info.get_weather_data('London')
        assert result == empty_weather_response


def test_get_weather_data_error(weather_info):
    # Test that get_weather_data handles a request error properly.
    with mock.patch('requests.get', side_effect=mock_get_error):
        result = weather_info.get_weather_data('London')
        assert result is None


def test_process_weather_data_success(weather_info):
    # Test that process_weather_data processes weather data correctly.
    with mock.patch('requests.get', side_effect=mock_get_success):
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


def test_process_weather_data_empty(weather_info):
    # Test that process_weather_data handles an empty weather data response.
    with mock.patch('requests.get', side_effect=mock_get_empty):
        weather_data = weather_info.get_weather_data('London')
        result = weather_info.process_weather_data(weather_data)
        assert result == []


def test_process_weather_data_malformed(weather_info):
    # Test that process_weather_data handles a malformed weather data response.
    with mock.patch('requests.get', side_effect=mock_get_malformed):
        weather_data = weather_info.get_weather_data('London')
        result = weather_info.process_weather_data(weather_data)
        assert result == []


def test_check_for_bad_weather_success(weather_info):
    # Test that check_for_bad_weather identifies bad weather correctly.
    with mock.patch('requests.get', side_effect=mock_get_success):
        weather_data = weather_info.get_weather_data('London')
        processed_data = weather_info.process_weather_data(weather_data)
        result = weather_info.check_for_bad_weather(processed_data)
        expected = []  # Update with expected bad weather alerts if any
        assert result == expected


def test_provide_planting_advice_success(weather_info, planting):
    # Test that provide_planting_advice gives correct planting advice.
    with mock.patch('requests.get', side_effect=mock_get_success):
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
    (malformed_weather_response, []),
])
def test_map_weather_data(weather_info, input_data, expected_output):
    #Test the mapping of weather data from the API response to the expected format.
    if input_data == successful_weather_response:
        result = weather_info.process_weather_data(input_data)
    else:
        result = weather_info.process_weather_data({'list': input_data})
    assert result == expected_output
