# Importing all necessary modules and packages
from http.client import HTTPException
import requests
from requests import RequestException
from config import weather_api_key, base_weather_url
from collections import Counter


class WeatherInfo:

    def __init__(self):
        self.api_key = weather_api_key
        self.base_weather_url = base_weather_url

    # Function to fetch the weather data for a specific location from openWeatherMap API.
    def get_weather_data(self,location):
        try:
            # Defining the API request URL with proper parameters
            url = base_weather_url + "&appid=" + weather_api_key + "&q=" + location + "&units=" + "metric"
            response = requests.get(url)
            result = response.json()
            # print(response)
            # If the response status code is not 200 i.e., not success
            if response.status_code != 200:
                print(f"Error fetching data: {response.status_code} - {response.reason}")
                return result["message"]
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

