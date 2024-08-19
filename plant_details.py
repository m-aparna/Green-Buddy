import requests
from http.client import HTTPException

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
        except requests.exceptions.RequestException as request_error:
            print(f"Request error: {request_error}")
        except HTTPException as http_error:
            print(f"HTTP error: {http_error}")
        except ValueError as json_error:
            print(f"JSON decode error: {json_error}")
        except Exception as error:
            print(f"An unexpected error occurred: {str(error)}")
        return None
    
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
            except requests.exceptions.RequestException as request_error:
                print(f"Request error: {request_error}")
            except HTTPException as http_error:
                print(f"HTTP error: {http_error}")
            except ValueError as json_error:
                print(f"JSON decode error: {json_error}")
            except Exception as error:
                print(f"An unexpected error occurred: {str(error)}")
            return None
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
            except requests.exceptions.RequestException as request_error:
                print(f"Request error: {request_error}")
            except HTTPException as http_error:
                print(f"HTTP error: {http_error}")
            except ValueError as json_error:
                print(f"JSON decode error: {json_error}")
            except Exception as error:
                print(f"An unexpected error occurred: {str(error)}")
            return None

def plant_search(query, api_key):
    plant = Plant(query, api_key)
    details = plant.complete_details()
    care = plant.caring_details()
    return [details, care]
