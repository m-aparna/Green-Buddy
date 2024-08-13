from flask import Flask, request, render_template
from weather import get_weather_data, process_weather_data, check_for_bad_weather, get_planting_advice
from places import get_places_info_for_location
from config import google_maps_api_key

# Initialize the Flask application
app = Flask(__name__)


# Route to render the homepage for weather information
@app.route('/')
def weather_homepage():
    return render_template('weather_index.html')   # Renders the weather index page using render_template

# Route to render the homepage for nearby shops
@app.route('/shops')
def shops_homepage():
    return render_template('shops_index.html')

# Route to display weather information
@app.route('/weather_info', methods=['GET', 'POST'])
def weather_info():
    try:
        location = request.form.get('location')
        if not location:
            raise ValueError("Location is required.")
        weather_data = get_weather_data(location)
        if not weather_data:
            return "Failed to fetch weather data for this location Please enter correct location."

        forecast = process_weather_data(weather_data)
        alerts = check_for_bad_weather(forecast)
        advice = get_planting_advice(forecast)

        return render_template('weather_info.html', location=location, forecast=forecast, alerts=alerts, advice=advice)
    except Exception as error:
        return f"Something went wrong: {error}"

# Route to handle the form submission and display nearby shop information
@app.route('/nearby_shops', methods=['GET', 'POST'])
def shops_info():
    try:
        location = request.form.get('nearbyshops')
        shops_data = get_places_info_for_location(location)

        if not shops_data:
            return "Failed to fetch shops data for this location."

        map_url = f"https://www.google.com/maps/embed/v1/search?key={google_maps_api_key}&q=garden+shops+in+{location}"

        return render_template('shops_info.html', location=location, shops=shops_data, map_url=map_url)
    except Exception as error:
        return f"Something went wrong while processing your request : {error}"


if __name__ == '__main__':
    app.run(debug=True)
