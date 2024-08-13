import requests
from requests import RequestException
from config import api_key, base_url
from collections import Counter


def get_weather_data(location):
    try:
        # fetching weather data for a specific location
        url = base_url + "&appid=" + api_key + "&q=" + location + "&units=" + "metric"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code} - {response.reason}")
            return None
        return response.json()
    except RequestException as req_err:
        # Handle request-related errors
        print(f"Request error: {req_err}")
        return None
    except ValueError as val_err:
        # Handle JSON decoding errors
        print(f"JSON decoding error: {val_err}")
        return None

    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error: {e}")
        return None



def process_weather_data(data):
    try:
        mapped_data = {}
        for weather_values in data['list']:
            date = weather_values['dt_txt'].split(' ')[0]
            if date not in mapped_data:
                mapped_data[date] = []
            mapped_data[date].append({
                'temperature': weather_values['main']['temp'],
                'weather': weather_values['weather'][0]['description'],
                'pressure': weather_values['main']['pressure'],
                'humidity': weather_values['main']['humidity'],
                'wind_speed': weather_values['wind']['speed'],
                'icon': weather_values['weather'][0]['icon']
            })

        weather_forecast = []

        for date, values in mapped_data.items():
            temperature_total = pressure_total = humidity_total = wind_speed_total = 0
            weather_count = Counter()
            icon_count = Counter()

            for value in values:
                temperature_total += value['temperature']
                pressure_total += value['pressure']
                humidity_total += value['humidity']
                wind_speed_total += value['wind_speed']
                weather_count[value['weather']] += 1
                icon_count[value['icon']] += 1

            avg_temp = round((temperature_total / len(values)), 2)
            avg_pressure = round((pressure_total / len(values)), 2)
            avg_humidity = round((humidity_total / len(values)), 2)
            avg_wind_speed = round((wind_speed_total / len(values)), 2)
            most_common_weather = weather_count.most_common(1)[0][0]
            most_common_icon = icon_count.most_common(1)[0][0]

            weather_forecast.append({
                'date': date,
                'temperature': avg_temp,
                'pressure': avg_pressure,
                'humidity': avg_humidity,
                'wind_speed': avg_wind_speed,
                'weather': most_common_weather,
                'icon': most_common_icon
            })

        return weather_forecast

    except KeyError as key_err:
        # Handle missing data keys
        print(f"Key error during data processing: {key_err}")
        return []

    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error during data processing: {e}")
        return []


def check_for_bad_weather(forecast):
    bad_weather_conditions = ['Thunderstorm', 'lightning', 'rain', 'snow', 'light rain', 'moderate rain',
                              'Drizzle', 'heavy rain', 'wind', 'landslide', 'snow fall', 'snow', 'tornado', 'mist',
                              'smoke', 'haze', 'Dust', 'fog', 'sand', 'ash', 'squall']
    alerts_info = []
    try:
        for day in forecast:
            weather_information = day['weather'].lower()
            for words in bad_weather_conditions:
                if words in weather_information:
                    alerts_info.append({
                        'date': day['date'],
                        'alert_text': f"Bad weather is expected on {day['date']}. Please be careful and try to avoid planting."
                    })
                    break
        return alerts_info

    except KeyError as key_err:
        # Handle missing data keys
        print(f"Key error during weather checking: {key_err}")
        return []

    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error during weather checking: {e}")
        return []



def get_planting_advice(forecast):
    suggestion = []
    try:
        for day in forecast:
            temperature = day['temperature']
            humidity = day['humidity']
            weather = day['weather']

            if weather in ['clear sky', 'clouds', 'overcast clouds', 'broken clouds', 'scattered clouds', 'few clouds']:
                if 10 <= temperature <= 25 and 60 <= humidity <= 70:
                    phase = 'Vegetative phase'
                    plant_suggestion = 'tomatoes or basil'
                    suggestion.append({
                        'date': day['date'],
                        'advice': f'Good weather for planting during the {phase}. Consider planting {plant_suggestion}.',
                        'phase': phase,
                        'plant_suggestion': plant_suggestion
                    })
                elif 25 <= temperature <= 30 and 40 <= humidity <= 50:
                    phase = 'Flowering phase'
                    plant_suggestion = 'flowers or herbs'
                    suggestion.append({
                        'date': day['date'],
                        'advice': f'Based on temperature and humidity, consider planting some flowers or herbs in the current {phase}.',
                        'phase': phase,
                        'plant_suggestion': plant_suggestion
                    })
                else:
                    phase = 'General gardening'
                    plant_suggestion = 'carrots or spinach'
                    suggestion.append({
                        'date': day['date'],
                        'advice': f'Based on temperature and humidity, consider general gardening practices and planting hardier vegetables like {plant_suggestion}.',
                        'phase': phase,
                        'plant_suggestion': plant_suggestion
                    })
            else:
                suggestion.append({
                    'date': day['date'],
                    'advice': 'Considering temperature and humidity, it is not a good weather for planting. Consider waiting for a clearer day.'
                })
        return suggestion

    except KeyError as key_err:
        # Handle missing data keys
        print(f"Key error during planting advice generation: {key_err}")
        return []

    except Exception as e:
        # Handle any other unexpected errors
        print(f"Unexpected error during planting advice generation: {e}")
        return []