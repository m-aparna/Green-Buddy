# Class and methods related to analyzing the processed weather data and generating planting advice.
class PlantingAdvice:
    # Function to check for bad weather conditions in the processed forecast based on some keywords as per response
    # returned A static method can be called directly from the class, without having to create an instance of the
    # class.It does not require an instance of the class to be called, nor does it have access to an instance.
    @staticmethod
    def check_for_bad_weather(forecast):
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
            print(f"Key error during weather checking: {key_error}")
            return []
        except Exception as error:
            print(f"Unexpected error during weather checking: {error}")
            return []

    # function to generate exceptions and provide planting advice. Calls functions _generate_advice_for_day to generate advice based on forecast
    @staticmethod
    def provide_planting_advice(forecast):
        try:
            return PlantingAdvice._generate_advice_for_day(forecast)
        except KeyError as key_error:
            # handle key error
            print(f"Key error during planting advice generation: {key_error}")
            return []
        except Exception as error:
            # hanle any other error
            print(f"Unexpected error during planting advice generation: {error}")
            return []

    # function to generate planting advice based on  temperature and humidity conditions
    @staticmethod
    def _generate_advice_for_day(forecast):
        suggestion = []
        for day in forecast:
            # Loop through each date in the forecast to generate planting advice
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
                        'advice': f"Good weather for planting during the {phase}. Consider planting {plant_suggestion}.",
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
