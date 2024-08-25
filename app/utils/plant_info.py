import requests
from http.client import HTTPException

class Plant_Basic_Info:
    def __init__(self, name, api_key):
        self.name = name
        self.api_key = api_key
        self.url = "https://perenual.com/api/"  # URL for searching plants
        self.id = self.plant_id()

    def plant_id(self):
        try:
            response = requests.get(f"{self.url}species-list?key={self.api_key}&q={self.name}") # Make a GET request to the API
            response.raise_for_status() # This will raise an HTTPError for bad responses
            data = response.json()   # Parse the JSON response from the HTTP request and store it in the 'data' variable
            if 'data' in data and data['data']:  # checks if the key 'data' exists in the list dictionary and this value is not empty or None.
                return data['data'][0]['id']    # Return the ID of the matching plant
            else:
                print(f"{self.name} plant information is not found")
                return None
        except requests.exceptions.RequestException as request_error:
            print(f"Request error: {request_error}")
        except HTTPException as http_error:
            print(f"HTTP error: {http_error}")
        except ValueError as json_error:
            print(f"JSON decode error: {json_error}")
        except Exception as error:
            print(f"An unexpected error occurred: {str(error)}")
        return None

    def basic_details(self):
        if self.id:
            try:
                response = requests.get(f"{self.url}species/details/{self.id}?key={self.api_key}")
                response.raise_for_status()
                plant_info = response.json()

                Common_name = plant_info.get('common_name', 'N/A')
                Scientific_name = plant_info.get('scientific_name', 'N/A')
                Other_names = plant_info.get('other_name', 'N/A')
                Family = plant_info.get('family', 'N/A')
                Origin = plant_info.get('origin', 'N/A')
                Type = plant_info.get('type', 'N/A')
                Description = plant_info.get('description', 'N/A')
                Image =  plant_info.get('default_image', {}).get('original_url', 'N/A')
            
                return [Common_name, Scientific_name, Other_names, Family, Origin, Type, Description, Image]
                
            except requests.exceptions.RequestException as request_error:
                print(f"Request error: {request_error}")
            except HTTPException as http_error:
                print(f"HTTP error: {http_error}")
            except ValueError as json_error:
                print(f"JSON decode error: {json_error}")
            except Exception as error:
                print(f"An unexpected error occurred: {str(error)}")
            return None
    
