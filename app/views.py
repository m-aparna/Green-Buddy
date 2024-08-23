# Contains all standard url endpoints
# Homepage, Guest, User

from flask import Blueprint, render_template, request, flash, redirect
from app.utils.plant_care import youtube_search, plant_search
from config import youtube_api_key, plant_api_key, google_api_key,base_places_url
from flask_login import login_required, current_user
from .models import Note
from . import db
from app.utils.plant_info import Plant_Basic_Info
from app.utils.planting_advice import PlantingAdvice
from app.utils.weather import WeatherInfo
from app.utils.shops import ShopsInfo

# Create a blueprint
views = Blueprint('views', __name__)

# Create a route for homepage
@views.route('/')
def homepage():
    return render_template('homepage.html', user='')

# Create a route for plant info
@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['plant_name']
        plant_info = Plant_Basic_Info(query, plant_api_key)
        plant_details = plant_info.basic_details()

        if plant_details:
            return render_template('plant_info.html', plant_details=plant_details, plant_name=query)
        else:
            error_message = "Sorry, details were not found or an error occurred."
            return render_template('plant_info.html', error = error_message, plant_name=query)

    return render_template('plant_info.html')

# Create a route for dashboard
@views.route('/dashboard', methods=['GET', 'POST'])
@login_required # Can only be accessed if user is logged in
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

# Route to delete note
@views.route('/delete-note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    # Query the note by ID
    note = Note.query.get(note_id)

    if note:
        # Delete the note from the database
        db.session.delete(note)
        db.session.commit()

    return redirect('/dashboard')

# Create a route for plant care page
@views.route('/plant-care', methods=['GET', 'POST'])
@login_required # Can only be accessed if user is logged in
def plant_care():
        video_ids = []
        plant_data = ''
        query = None
        if request.method == 'POST':
            query = request.form.get('query') # Get query from Search box
            # Plant API
            plant_data = plant_search(query, plant_api_key)
            # Youtube API
            video_ids = youtube_search(query + ' plant care', youtube_api_key) # Get Video IDs from Python function
        return render_template('plant_care.html', query=query, plant_data=plant_data, video_ids=video_ids, user='')

# Create a route for weather page
@views.route('/weather', methods=['GET', 'POST'])
@login_required # Can only be accessed if user is logged in
def weather():
    try:

        location = request.form.get('location')
        if location:
            weather_info = WeatherInfo()
            planting = PlantingAdvice()
            weather_data = weather_info.get_weather_data(location)
            # Error handling for wrong location
            if weather_data == "city not found":
                return render_template('weather.html',error="City not found")
            else:
                forecast = weather_info.process_weather_data(weather_data)
                alerts = planting.check_for_bad_weather(forecast)
                advice = planting.provide_planting_advice(forecast)
                return render_template('weather.html', location=location, forecast=forecast, alerts=alerts, advice=advice)
        else:
            return render_template('weather.html', location=location, forecast='', alerts='', advice='')

    except Exception as error:
        return f"Something went wrong: {error}"

# Create a route for shops page
@views.route('/shops', methods=['GET', 'POST'])
@login_required # Can only be accessed if user is logged in
def shops():
    try:
        location = request.form.get('nearby shops')
        if location:
            shops_info = ShopsInfo(base_places_url, google_api_key)
            shops_data = shops_info.get_shops_data(location)
            if not shops_data:
                return "city not found"

            display_map = shops_info.embed_map_url(location)

            return render_template('shops.html', location=location, shops=shops_data, map_url=display_map)
        else:
            return render_template('shops.html', location=location, shops='', map_url='')
    except Exception as error:
        return f"Something went wrong while processing the request : {error}"
