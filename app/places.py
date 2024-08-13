import json
import requests
from config import base_places_url, places_api_key


def get_places_data(location):
    # 'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel,places.googleMapsUri,'
    # 'places.currentOpeningHours,places.rating'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': places_api_key,
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel,places.googleMapsUri,places.rating,places.nationalPhoneNumber,places.photos,places.currentOpeningHours'
    }

    payload = {
        "textQuery": "Garden shops in " + location,
        "maxResultCount": "3"
    }
    response = requests.post(base_places_url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return None
    return response.json()


def get_places_info_for_location(location):
    mappeddata = []
    shops_location = get_places_data(location)

    if not shops_location:
        return f"No shops found for this location"

    for place in shops_location.get('places', []):
        #.get() method is used to provide default values directly
        # Extracting and formatting the weekday descriptions
        opening_hours = place.get('currentOpeningHours', {}).get('weekdayDescriptions', [])
        opening_hours_formatted = "\n".join(opening_hours)

        # photo_name = 'Photo not available'
        photo_url = '#'
        if 'photos' in place and place['photos']:
            photo_ref = place['photos'][0]['name']
            photo_url = f"https://places.googleapis.com/v1/{photo_ref}/media?key={places_api_key}&maxHeightPx=400&maxWidthPx=400"
            #photo_name = place['photos'][0]['authorAttributions'][0]['displayName']

        map_info = {
            'name': place.get('displayName', {}).get('text', 'N/A'),
            'address': place.get('formattedAddress', 'N/A'),
            'rating': place.get('rating', 'N/A'),
            'google_maps_uri': place.get('googleMapsUri', 'Not available'),
            'opening_hours': opening_hours_formatted,
            'contact_number': place.get('nationalPhoneNumber', 'N/A'),
            #'photo_name': photo_name,
            'photo_url': photo_url
        }
        mappeddata.append(map_info)

    return mappeddata
