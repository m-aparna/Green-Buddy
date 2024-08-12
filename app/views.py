# Contains all standard url endpoints
# Homepage, Guest, User

from flask import Blueprint, render_template, request
from .plant_care import youtube_search, plant_search
from config import youtube_api_key, plant_api_key

# Create a blueprint
views = Blueprint('views', __name__)

# Create a route for homepage
@views.route('/')
def homepage():
    return render_template('homepage.html')

# Create a route for plant care page
@views.route('/plant-care', methods=['GET', 'POST'])
def plant_care():
    video_ids = []
    plant_data = ''
    if request.method == 'POST':
        query = request.form.get('query') # Get query from Search box
        # Plant API
        plant_data = plant_search(query, plant_api_key)
        # Youtube API
        video_ids = youtube_search(query + ' plant care', youtube_api_key) # Get Video IDs from Python function
    return render_template('plant_care.html', plant_data=plant_data, video_ids=video_ids)

