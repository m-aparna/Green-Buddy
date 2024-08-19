# Contains all standard url endpoints
# Homepage, Guest, User

from flask import Blueprint, render_template, request, flash, json, jsonify, redirect, url_for
from .plant_care import youtube_search, plant_search
from config import youtube_api_key, plant_api_key
from flask_login import login_required, current_user
from .models import Note
from . import db

# Create a blueprint
views = Blueprint('views', __name__)

# Create a route for homepage
@views.route('/')
def homepage():
    return render_template('homepage.html', user='')

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
        if request.method == 'POST':
            query = request.form.get('query') # Get query from Search box
            # Plant API
            plant_data = plant_search(query, plant_api_key)
            # Youtube API
            video_ids = youtube_search(query + ' plant care', youtube_api_key) # Get Video IDs from Python function
        return render_template('plant_care.html', plant_data=plant_data, video_ids=video_ids, user='')

# Create a route for weather page
@views.route('/weather', methods=['GET', 'POST'])
@login_required # Can only be accessed if user is logged in
def weather():
    return redirect(url_for('auth.login'))