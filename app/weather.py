# Importing all necessary modules and packages
from http.client import HTTPException
import requests
from requests import RequestException
from config import api_key, base_weather_url
from collections import Counter


class WeatherInfo:

    def __init__(self):
        self.api_key = api_key
        self.base_weather_url = base_weather_url

    # Function to fetch the weather data for a specific location from openWeatherMap API.
    def get_weather_data(self,location):
        try:
            # Defining the API request URL with proper parameters
            url = base_weather_url + "&appid=" + api_key + "&q=" + location + "&units=" + "metric"
            response = requests.get(url)
            print(response)
            # If the response status code is not 200 i.e., not success
            if response.status_code != 200:
                print(f"Error fetching data: {response.status_code} - {response.reason}")
                return None
            return response.json()  # Return JSON response if the request was successful.
        except RequestException as request_error:
            # Handle request-related errors
            print(f"Request error: {request_error}")
            return None
        except TimeoutError as timeout_error:
            # Handle request-related errors
            print(f"Timeout error: {timeout_error}")
            return None
        except ValueError as value_error:
            # Handle JSON related errors
            print(f"JSON decoding error: {value_error}")
            return None
        except HTTPException as http_error:
            print(f"HTTP error: {http_error}")
        except Exception as error:
            # Handle any unexpected errors
            print(f"Unexpected error: {error}")
            return None
        except ConnectionError as conn_error:
            # Handle any connection errors
            print(f"Unexpected connection error: {conn_error}")
            return None

    # Function to process and analyze the fetched weather data for 5 days with 3-hour steps.It returns average values
    # for each day based on 24-hour data.
    # The Parameter passed in the function is the response returned by the API.
    # The Function returns a list of dictionaries containing the average weather values for each day.

    def process_weather_data(self, weather_data):
        try:
            daily_data = self._organize_weather_data_by_date(weather_data)
            return self._calculate_daily_averages(daily_data)
        # Handle missing data keys
        except KeyError as key_error:
            print(f"Key error during data processing: {key_error}")
            return []
        # Handle any other unexpected errors during processing of weather forecast data
        except Exception as error:
            print(f"Unexpected error during data processing: {error}")
            return []

    # Function to organize weather data by date
    def _organize_weather_data_by_date(self, data):
        daily_weather_data = {}
        for weather_values in data['list']:
            # print(f"Processing entry: {weather_values}")
            # To extract the date part
            date = weather_values['dt_txt'].split(' ')[0]
            if date not in daily_weather_data:
                daily_weather_data[date] = []
            # Adding the weather details for each day in the mapped_data dictionary with key and values.
            daily_weather_data[date].append({
                'temperature': weather_values['main']['temp'],
                'weather': weather_values['weather'][0]['description'],
                'period_of_day': weather_values['sys']['pod'],
                'pressure': weather_values['main']['pressure'],
                'humidity': weather_values['main']['humidity'],
                'wind_speed': weather_values['wind']['speed'],
                'icon': weather_values['weather'][0]['icon']
            })
        return daily_weather_data

    # Function to calculate the daily averages values for temperature,humidity etc.
    def _calculate_daily_averages(self, daily_data):
        weather_forecast = []
        # for iterating through key,value in daily_data dictionaries we use .items()
        for date, values in daily_data.items():
            temp_total = pressure_total = humidity_total = wind_speed_total = 0
            # Create a new, empty Counter object
            weather_icon_counter = Counter()
            for value in values:
                temp_total += value['temperature']
                pressure_total += value['pressure']
                humidity_total += value['humidity']
                wind_speed_total += value['wind_speed']
                weather_icon_counter[(value['weather'], value['icon'])] += 1

            avg_temp = int(temp_total / len(values))
            avg_pressure = round(pressure_total / len(values), 2)
            avg_humidity = round(humidity_total / len(values), 2)
            avg_wind_speed = round(wind_speed_total / len(values), 2)

            # Determine the most common (weather, icon) pair
            most_common_weather_icon = weather_icon_counter.most_common(1)[0][0]
            most_common_weather = most_common_weather_icon[0]
            most_common_icon = most_common_weather_icon[1]
            # print(most_common_icon)
            # Add the processed average values for the current date to the weather_forecast list.
            weather_forecast.append({
                'date': date,
                'temperature': avg_temp,
                'pressure': avg_pressure,
                'humidity': avg_humidity,
                'wind_speed': avg_wind_speed,
                'weather': most_common_weather,
                'icon': most_common_icon
            })
        # print(weather_forecast)
        # Return the processed weather forecast data
        return weather_forecast

    # Function to check for bad weather conditions in the processed forecast based on some keywords as per response returned
    def check_for_bad_weather(self,forecast):
        # List of weather conditions considered "bad" as per the OpenWeatherMap API documentation
        bad_weather_conditions = ['Thunderstorm', 'lightning', 'rain', 'snow', 'light rain', 'moderate rain',
                                  'Drizzle', 'heavy rain', 'wind', 'landslide', 'snow fall', 'snow', 'tornado', 'mist',
                                  'smoke', 'haze', 'Dust', 'fog', 'sand', 'volcanic ash', 'squall']
        alerts_info = []
        try:
            # Loop through each date forecast to identify bad weather
            for day in forecast:
                weather_information = day['weather'].lower()
                for words in bad_weather_conditions:
                    if words in weather_information:
                        # If bad weather or the keywords mentioned above are found, then add an alert to the list
                        # alerts_info
                        alerts_info.append({
                            'date': day['date'],
                            'alert_text': f"Bad weather is expected on {day['date']}. Please be careful and try to avoid "
                                          f"planting."
                        })
                        break
            return alerts_info
        except KeyError as key_error:
            # Handle missing data keys
            print(f"Key error during weather checking: {key_error}")
            return []

        except Exception as error:
            # Handle any other unexpected errors
            print(f"Unexpected error during weather checking: {error}")
            return []
    # function to generate exceptions and provide planting advice. Calls functions _generate_advice_for_day to generate advice based on forecast
    def provide_planting_advice(self, forecast):
        try:
            return self._generate_advice_for_day(forecast)
        # Handle missing data keys
        except KeyError as key_error:
            print(f"Key error during planting advice generation: {key_error}")
            return []
        # Handle any other unexpected errors
        except Exception as error:
            print(f"Unexpected error during planting advice generation: {error}")
            return []

    def _generate_advice_for_day(self, forecast):
            suggestion = []
            # Loop through each date in the forecast to generate planting advice
            for day in forecast:
                temperature = day['temperature']
                humidity = day['humidity']
                weather = day['weather']
                # Advice based on temperature, weather condition, humidity factors
                # If weather description has any of these keywords then proceed to give advice else suggest bad weather
                if weather in ['clear sky', 'clouds', 'overcast clouds', 'broken clouds', 'scattered clouds',
                               'few clouds']:
                    if 18 <= temperature <= 25 and 60 <= humidity <= 70:
                        phase = 'Vegetative phase'
                        plant_suggestion = 'tomatoes or basil'
                        suggestion.append({
                            'date': day['date'],
                            'advice': f"Good weather for planting during the {phase}.Consider planting {plant_suggestion}.",
                            'phase': phase,
                            'plant_suggestion': plant_suggestion
                        })
                    elif 25 <= temperature <= 30 and 40 <= humidity <= 50:
                        phase = 'Flowering phase'
                        plant_suggestion = 'flowers or herbs'
                        suggestion.append({
                            'date': day['date'],
                            'advice': f"Based on temperature and humidity, consider planting some flowers or herbs in the "
                                      f"current {phase}.",
                            'phase': phase,
                            'plant_suggestion': plant_suggestion
                        })
                    else:
                        phase = 'General gardening'
                        plant_suggestion = 'carrots or spinach'
                        suggestion.append({
                            'date': day['date'],
                            'advice': f"Based on temperature and humidity, consider general gardening practices and "
                                      f"planting hardier vegetables like {plant_suggestion}.",
                            'phase': phase,
                            'plant_suggestion': plant_suggestion
                        })
                # Suggestion to wait for favourable weather
                else:
                    suggestion.append({
                        'date': day['date'],
                        'advice': f"Based on weather conditions, it is not a good weather for planting. Consider "
                                  "waiting for a clearer day."
                    })
            return suggestion

