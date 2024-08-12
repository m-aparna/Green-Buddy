# YouTube API search function
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# Plant API
import requests

class Plant:
    def __init__(self, name, api_key):
        self.name = name
        self.api_key = api_key
        self.url = "https://perenual.com/api/"
        self.id = self.plant_id()

    def plant_id(self):
        try:
            response = requests.get(f"{self.url}species-list?key={self.api_key}&q={self.name}")    # Make a GET request to the API
            response.raise_for_status() # This will raise an HTTPError for bad responses
            data = response.json()   # Parse the JSON response from the HTTP request and store it in the 'data' variable
            if 'data' in data and data['data']:  # checks if the key 'data' exists in the list dictionary and this value is not empty or None.
                return data['data'][0]['id']    # Return the ID of the matching plant
            else:
                return f"{self.name} plant information is not found"
        except Exception as e:  # Catches unexpected errors.
            return f"{str(e)}"
    
    # general details
    def complete_details(self):
        if self.id:
            try:
                response = requests.get(f"{self.url}species/details/{self.id}?key={self.api_key}")    # API endpoint to get detailed information using the plant ID
                response.raise_for_status() # This will raise an HTTPError for bad responses
                plant_details = response.json()
            # Print specific details about the plant
                common_name = plant_details.get('common_name', 'N/A')
                scientific_name = plant_details.get('scientific_name', 'N/A')
                sunlight = plant_details.get('sunlight', 'N/A')
                watering = plant_details.get('watering', 'N/A')
                pruning_month = plant_details.get('pruning_month', 'N/A')
                maintenance = plant_details.get('maintenance', 'N/A')
                image = plant_details.get('default_image', {}).get('original_url', 'N/A')
                return [common_name, scientific_name, sunlight, watering, pruning_month, maintenance, image]
            except Exception as e:
                return f"{str(e)}"
    
    # Care details
    def caring_details(self):
        if self.id:
            try:
                response = requests.get(f"{self.url}species-care-guide-list?species_id={self.id}&key={self.api_key}")
                response.raise_for_status()  # Raise an exception for HTTP errors
                care_info = response.json()  # Parse the JSON response
                if 'data' in care_info and care_info['data']:
                    sections = care_info['data'][0].get('section', [])
                    types = ['watering', 'sunlight', 'pruning']
                    result = []
                    for section in sections:
                        if section['type'] in types:
                            result.append(f"{section['type'].capitalize()} Description: {section.get('description', 'N/A')}")
                    return result
                else:
                    return f"Care details are not found for {self.name} plant"
            except Exception as e:
                return f"{str(e)}"

def plant_search(query, api_key):
    plant = Plant(query, api_key)
    details = plant.complete_details()
    care = plant.caring_details()
    return [details, care]


# YouTube API
def youtube_search(query, API_KEY):
    # Create service object and use search function
    service = build('youtube', 'v3', developerKey=API_KEY).search()

    # Create request object
    request = service.list(q= f'{query}', part='snippet', type='video', maxResults=2, order='rating', videoDuration='medium', relevanceLanguage='en')

    # Execute the request
    try:
        response = request.execute()
        items = response['items']
        video_ids = []
        for i in items:
            video_ids.append(i["id"]["videoId"])    
        return video_ids
    except HttpError as error:
        return f"Status code {error.status_code}, details - {error.error_details}"
    finally:
        # Close service
        service.close()

