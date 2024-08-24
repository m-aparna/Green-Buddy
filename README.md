# Green Buddy

Green Buddy is a one-stop solution for gardeners, especially new gardeners who want to access all gardening knowledge they need at one place.
This platform provides various services to support healthy plant growth and effective gardening practices. Two such features are weather forecast for 5 days and nearby local gardening shops.

Feature:

1. Weather Forecast: Get a detailed 5-day weather forecast for your gardening needs. This feature provides insights into upcoming weather conditions, helping you make informed decisions about plant care.

2. Nearby Gardening Shops: Easily find local gardening shops with information such as ratings, addresses, and opening hours. This helps to locate the right resources for gardening needs.


## API used

For weather API, I have used free open source API 

https://openweathermap.org/forecast5

For Nearby shops I have used free open source google places API

https://developers.google.com/maps/documentation/places/web-service/overview

For embedding the map in the website I have used Google Maps Embed  API

https://developers.google.com/maps/documentation/embed/get-started

For validating user inout location Geocoding API is used.

https://developers.google.com/maps/documentation/geocoding/start



### Tools/Technologies used

#### Front end:
- HTML (Jinja2 Templating language)
- Bootstrap v5.0
- CSS


#### Backend:

- Python v3.12.x
- Flask v3.0.x
- pytest v8.0.x
- SQLAlchemy v2.0.x


#### Other Tools:
- Git Hub VCS
- Jira
- Pycharm IDE/Visual Studio Code


### Libraries/Packages to be installed:


1. Install (https://www.python.org/downloads/)[Python]>=3

2. Flask: 

Install Flask. It  is a web framework used to build the web application.

    
        pip install flask


2. Requests module: 


This module allows you to make HTTP requests. [requests 2.32.3](https://pypi.org/project/requests/)


       pip install requests


3. RequestException:


This exception is used for handling errors in HTTP requests. It is available in the requests module.


       from requests import RequestException


4. pytest: Pytest is a testing framework that makes it easy to write simple and scalable test cases.
Install pytest using pip:



        pip install pytest


5. Import Mock:

Import Mock: Used for creating mock objects during testing.

        from unittest import mock

6. json Module:
This module is part of the Python Standard Library and is used for encoding and decoding JSON data.
You don't need to install it separately, as it comes with Python by default. Import it using:

       import json


### API Key Generation:

**Openweather API Key Generation-**

1. Sign Up/Log In:

   - Visit the [OpenWeather website](https://home.openweathermap.org/users/sign_up).
   - Sign up for a new account or log in if you already have one.
   - 
2. Access API Keys:

    - After logging in, go to the API keys section of your account dashboard.
   
3. Create a New Key:

   - Click on Create Key or Add New Key.
   - Enter a name for the key (e.g., "WeatherApp").
   
4. Retrieve API Key:

    - Copy the API key for use in your application.
   
**Note:** New users might need to enter billing information during the sign-up process.


## Installation/Setup:


### Clone the repository

        git clone https://github.com/m-aparna/Green-Buddy.git
 

### Go to the project root

        cd GreenBuddy

#### install the requirements and all dependencies

        pip3 install -r requirements.txt

### Configure API keys in config.py

 Replace 'google_api_key' with your own API key, Weather_api_key with your own API key.



###  Run flask application

        main.py

### Now the services are available. To access the weather information and nearby shops data user needs to login using username and password.For signup email id,username and password needs to be set.



### Endpoints

- Endpoint: http://127.0.0.1:5000/weather

    - Method Type: GET, POST
    - Details: This endpoint provides users with detailed weather information for the current day, including a 5-day forecast, weather alerts, and gardening suggestions based on predicted weather conditions.

  
- Endpoint: http://127.0.0.1:5000/shops

    - Method Type: GET, POST
    - Details: This endpoint helps users find nearby gardening shops based on their current location. It provides relevant details such as shop ratings, addresses, and opening hours to help users plan their visits and get the supplies they need without traveling far.




## Files used:

weather.py- 

This file contains the code necessary for processing and fetching weather data.It handles the interaction with weather APIs to retrieve and process weather-related information.

planting_advice.py—

This file includes the logic for checking weather conditions and generating alerts based on those conditions.
It also provides system-generated planting advice
to help users make informed decisions about their gardening activities.

shops.py-

This file manages the code for fetching information about nearby gardening shops.It processes data from APIs
to provide users with details about local gardening stores,
including their locations and other relevant information.

## Testing

- pytest- Used pytest as the testing framework for testing weather and places API functions.Pytest provides powerful features such as fixtures, parameterized testing, and plugins. Fixtures allow for setting up pre-test conditions and tearing them down after tests are executed, which can reduce code repetition and improve maintainability.
Parameterized testing allows running the same test function with different sets of inputs, which is useful for checking a wide range of scenarios efficiently.

       pip install pytest



## Image Attributions:

**Weather background image :** [Image by wirestock on Freepik](https://www.freepik.com/free-photo/macro-shot-water-droplets-leaves-green-plant_17116047.htm#from_view=detail_alsolike)

**Nearby Shops locator background image -** [Image by Canva.com](https://www.canva.com/design/DAGNq93YWdI/wU8uhS1sOE-UM70M1Mt85A/edit)

**Weather HERO image-** [Image by storyset on Freepik](https://www.freepik.com/free-vector/weather-concept-illustration_6982823.htm#fromView=search&page=1&position=0&uuid=43e7e0e2-392f-49c2-88e3-c46864275f5b)

**Nearby Shops hero image -** [Image by upklyak on Freepik](https://www.freepik.com/free-vector/flower-shop-facade-night-city-street-vector-cartoon-illustration-urban-floral-boutique-gift-storefront-with-illuminated-windows-garlands-striped-tent-door-flowerpots-shelf_66811049.htm#fromView=search&page=2&position=48&uuid=48f47d53-7e5d-48c4-a563-969639b77082)


      

      
