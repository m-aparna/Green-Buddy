import json
import requests
from requests import RequestException

from config import base_places_url, places_api_key, google_maps_api_key


class ShopsInfo:
    def __init__(self, places_api_key, base_places_url, google_maps_api_key):
        self.places_api_key = places_api_key
        self.base_places_url = base_places_url
        self.google_maps_api_key = google_maps_api_key

    # Function to fetch places information like garden shops from Google places API for a specific location
    def get_shops_data(self, location):
        try:
            shops_data = self._fetch_shops_data(location)
            if not shops_data:
                return "No shops found for this location."
            res = self._map_shops_data(shops_data)
            return res
        except Exception as error:
            print(f"Error while fetching place data: {error}")
            return None

    def _fetch_shops_data(self, location):
        try:
            # Fetches place data from the Google Places API based on the query.

            headers = self._build_headers()
            payload = self._create_payload(location)
            response = self._send_request(headers, payload)
            return response
        except Exception as error:
            print(f"Error in fetching shops data: {error}")
            return None

    # Headers required for the API request, including API key and fields to retrieve
    def _build_headers(self):
        # Headers required for the API request, including API key and fields to retrieve
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': self.places_api_key,
            'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel,places.googleMapsUri,'
                                'places.rating,places.nationalPhoneNumber,places.photos,places.currentOpeningHours'
        }
        return headers

    # Payload for the API request, specifying the query and maximum number of results
    def _create_payload(self,location):
        # Payload for the API request, specifying the query and maximum number of results
        payload = {
            "textQuery": "Garden shops in " + location,  # Query to search for garden shops in the specified location
            "maxResultCount": "3"                        # Maximum results to be returned
        }
        return payload

    def _send_request(self, headers, payload):
        try:
            # POST request(i.e send request) to the Google Places API
            response = requests.post(base_places_url, headers=headers, data=json.dumps(payload))
            print(response)
            # If the response status is success or not (for success status code is 200)
            if response.status_code != 200:
                print(f"Error fetching data: {response.status_code} - {response.text}")
                return None
            return response.json()          # return response data as json object if status code is 200
        except TimeoutError as timeout_error:
            # Handle request-related errors
            print(f"Timeout error: {timeout_error}")
            return None
        except RequestException as request_error:
            # Handle request-related errors
            print(f"Request error while: {request_error}")
            return None
        except ValueError as value_error:
            # Handle JSON related errors while parsing json data
            print(f"JSON decoding error: {value_error}")
            return None
        except Exception as error:
            # Handle any unexpected errors
            print(f"An Unexpected error occurred: {error}")
            return None
        except ConnectionError as conn_error:
            # Handle any connection errors
            print(f"Unexpected connection error: {conn_error}")
            return None
    # Function yo format the opening hours into proper format to be returned
    def _format_opening_hours(self, place):
        try:
            # Formats the opening hours of the place.
            # Extracting and formatting the weekday descriptions
            opening_hours = place.get('currentOpeningHours', {}).get('weekdayDescriptions', [])
            opening_hours_formatted = "\n".join(opening_hours)  # format the opening hours
            if opening_hours:
                return opening_hours_formatted
            else:
                return f"Not available"
        except Exception as error:
            print(f"Error formatting opening hours: {error}")
            return "Not available"
    def _generate_photo_url(self,places_data):
        try:
            # Initialize default values for photo-related information if not found
            photo_url = '#'
            if 'photos' in places_data and places_data['photos']:
                photo_ref = places_data['photos'][0]['name']
                photo_url = (f"https://places.googleapis.com/v1/{photo_ref}/media?key={self.places_api_key}&maxHeightPx=400"
                             f"&maxWidthPx=400")
            return photo_url
        except Exception as error:
            print(f"Error generating photo URL: {error}")
            return '#'

    """dictionary.get(keyname, value)
    get() method returns the value of the item with the specified key.Keyname of the item we want to return the value from
    value is a value to return if the specified key does not exist.
    Default value None"""
    def _map_shops_data(self, places_data):
        try:
            # Initialize an empty list to store the mapped data
            mapped_shops_data = []
            # Loop through each place found in the shops_location data
            for place in places_data.get('places', []):
                try:
                    # A dictionary to store the relevant information for each place
                    map_info = {
                        'name': place.get('displayName', {}).get('text', 'N/A'),
                        'address': place.get('formattedAddress', 'N/A'),
                        'rating': place.get('rating', 'N/A'),
                        'google_maps_uri': place.get('googleMapsUri', 'Not available'),
                        'opening_hours': self._format_opening_hours(place),
                        'contact_number': place.get('nationalPhoneNumber', 'N/A'),
                        'photo_url': self._generate_photo_url(place)
                    }
                    # Append the mapped information to the list
                    mapped_shops_data.append(map_info)

                except KeyError as key_error:
                    # Handle missing data keys
                    print(f"Key error during mapping of data: {key_error}")
                    return []
                except Exception as place_error:
                    print(f"Error processing place data: {place_error}")
                    continue
            # Return the list of mapped places data
            return mapped_shops_data
        except Exception as error:
            print(f"Error mapping shops data: {error}")
            return []
    def embed_map_url(self, location):
        try:
            # Generates a Google Maps embed URL for the specified location.
            map_url = f"https://www.google.com/maps/embed/v1/search?key={self.google_maps_api_key}&q=garden+shops+in+{location}"
            return map_url
        except Exception as error:
            print(f"Error generating embed map URL: {error}")
            return None