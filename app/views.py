# Contains all standard url endpoints
# Homepage, Guest, User

from flask import Blueprint, render_template, request, flash, json, jsonify, redirect, url_for
from .plant_care import youtube_search, plant_search
from config import youtube_api_key, plant_api_key, google_maps_api_key, places_api_key, base_places_url
from flask_login import login_required, current_user
from .models import Note
from . import db
from .shops import ShopsInfo
from .weather import WeatherInfo


# Create a blueprint
views = Blueprint('views', __name__)


# Create a route for homepage
@views.route('/')
def homepage():
    return render_template('homepage.html', user='')


# Create a route for plant care page
@views.route('/plant-care', methods=['GET', 'POST'])
def plant_care():
    video_ids = []
    plant_data = ''
    if request.method == 'POST':
        query = request.form.get('query')  # Get query from Search box
        # Plant API
        plant_data = plant_search(query, plant_api_key)
        # Youtube API
        video_ids = youtube_search(query + ' plant care', youtube_api_key)  # Get Video IDs from Python function
    return render_template('plant_care.html', plant_data=plant_data, video_ids=video_ids)


# Create a route for dashboard
@views.route('/dashboard', methods=['GET', 'POST'])
@login_required  # Can only be accessed if user is logged in
def dashboard():
    if request.method == 'POST':
        # Get the form data
        plant_name = request.form.get('plant_name')  # Get the title from the form
        plant_species = request.form.get('plant_species')  # Get the description from the form
        details = request.form.get('details')

        # Check if note has content / not
        if len(plant_name) < 1:
            flash("Plant Name cannot be empty!")
        elif len(plant_species) < 1:
            flash("Plant Species cannot be empty!")
        else:
            # Create a new Note instance with the data from the form
            new_note = Note(plant_name=plant_name, plant_species=plant_species, details=details)
            db.session.add(new_note)
            db.session.commit()
            return redirect('/dashboard')

    # Query all notes from the database
    notes = Note.query.all()
    return render_template('dashboard.html', user=current_user, notes=notes)


# View to delete note
@views.route('/delete-note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    # Query the note by ID
    note = Note.query.get(note_id)

    if note:
        # Delete the note from the database
        db.session.delete(note)
        db.session.commit()

    return redirect('/dashboard')

@views.route('/weather')
def weather_homepage():
    return render_template('weather_index.html')

@views.route('/shops')
def shops_homepage():
    return render_template('shops_index.html')

# Route to display weather information.Location is retrieved from the form as entered by user, and various functions
# to process the weather data, check for bad weather, and provide planting advice.

@views.route('/weather_info', methods=['GET', 'POST'])
def show_weather_info():
    try:
        location = request.form.get('location')
        if not location:
            raise ValueError("Location is required.")
        weather_info = WeatherInfo()
        weather_data = weather_info.get_weather_data(location)
        # print(weather_data)
        if not weather_data:
            return "Failed to fetch weather data for this location Please enter correct location."

        forecast = weather_info.process_weather_data(weather_data)
        alerts = weather_info.check_for_bad_weather(forecast)
        advice = weather_info.provide_planting_advice(forecast)

        return render_template('weather_info.html', location=location, forecast=forecast, alerts=alerts, advice=advice)
    except Exception as error:
        return f"Something went wrong: {error}"


# Route to handle the form submission and display nearby shop information Fetches shop information based on the
# location provided by the user and generates a Google Maps embed URL and necessary details of shop.


@views.route('/nearby_shops', methods=['GET', 'POST'])
def shops_info():
    try:
        location = request.form.get('nearby shops')
        if not location:
            raise ValueError("Location is required.")

        # shops_data = get_places_info_for_location(location)

        shops_info = ShopsInfo(places_api_key, base_places_url, google_maps_api_key)
        shops_data = shops_info.get_shops_data(location)
        if not shops_data:
            return "Failed to fetch shops data for this location."

        display_map = shops_info.embed_map_url(location)

        return render_template('shops_info.html', location=location, shops=shops_data, map_url=display_map)
    except Exception as error:
        return f"Something went wrong while processing the request : {error}"


