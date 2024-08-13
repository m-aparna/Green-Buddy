import json
import requests
from config import base_places_url, places_api_key


# Function to fetch places information like garden shops from Google places API for a specific location
def get_places_data(location):
    # Headers required for the API request, including API key and fields to retrieve
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': places_api_key,
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel,places.googleMapsUri,'
                            'places.rating,places.nationalPhoneNumber,places.photos,places.currentOpeningHours'
    }
    # Payload for the API request, specifying the query and maximum number of results
    payload = {
        "textQuery": "Garden shops in " + location,  # Query to search for garden shops in the specified location
        "maxResultCount": "3"  # Maximum results to be returned
    }
    # POST request to the Google Places API
    response = requests.post(base_places_url, headers=headers, data=json.dumps(payload))
    # If the response status is success or not (for success status code is 200)
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return None
    return response.json()  # return response data as json object if status code is 200


# Function to process and map the place data
def get_places_info_for_location(location):
    # Initialize an empty list to store the mapped data
    mapped_places_data = []
    shops_location = get_places_data(location)  # Get the place data for the specified location
    # if no shop data was found or an error occurred, return message for not getting shop information
    if not shops_location:
        return f"No shops found for this location"
    # Loop through each place found in the shops_location data
    for place in shops_location.get('places', []):
        # .get() method is used to provide default values directly
        # Extracting and formatting the weekday descriptions
        opening_hours = place.get('currentOpeningHours', {}).get('weekdayDescriptions', [])
        opening_hours_formatted = "\n".join(opening_hours)  # format the opening hours

        # photo_name = 'Photo not available'
        # Initialize default values for photo-related information if not found
        photo_url = '#'  # initializes the photo_url variable with a default placeholder value.useful in
        # front end.This is useful if the url doesn't have any photo.
        if 'photos' in place and place['photos']:
            photo_ref = place['photos'][0]['name']
            photo_url = (f"https://places.googleapis.com/v1/{photo_ref}/media?key={places_api_key}&maxHeightPx=400"
                         f"&maxWidthPx=400")
            # photo_name = place['photos'][0]['authorAttributions'][0]['displayName']
        # A dictionary to store the relevant information for each place
        map_info = {
            'name': place.get('displayName', {}).get('text', 'N/A'),  # get() is used to get the display name,
            # if not found replacement with 'N/A'
            'address': place.get('formattedAddress', 'N/A'),
            'rating': place.get('rating', 'N/A'),
            'google_maps_uri': place.get('googleMapsUri', 'Not available'),
            'opening_hours': opening_hours_formatted,
            'contact_number': place.get('nationalPhoneNumber', 'N/A'),
            'photo_url': photo_url
        }
        # Append the mapped information to the list
        mapped_places_data.append(map_info)
    # Return the list of mapped places data
    return mapped_places_data
