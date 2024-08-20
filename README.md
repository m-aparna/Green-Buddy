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



### Tools/Technologies used

Back-end:

Python 3.x

Flask framework

Pycharm



Front-end:

HTML

CSS

jinja2 template


### Libraries/Packages to be installed:


1. Install (https://www.python.org/downloads/)[Python]>=3

1. Flask: 

Flask is a web framework used to build the web application.

    
        pip install flask


2. Requests module: 


This module allows you to make HTTP requests. https://pypi.org/project/requests/


       pip install requests


3. RequestException:


This exception is used for handling errors in HTTP requests. It is available in the requests module.


       from requests import RequestException


4. pytest: For testing purposes, install pytest.



        pip install pytest


5. Import Mock:

Import Mock: Used for creating mock objects during testing.

        from unittest import mock




## Installation/Setup:


### Clone the repository

        git clone 

### Go to the project root

        cd GreenBuddy

#### install the requirements

        pip3 install -r requirements.txt

###  Run

        python3 main.py

### Now the services are available. To access the weather information and nearby shops data user needs to login using username and password.For signup email id,username and password needs to be set.



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




# Attributions:

<a href="https://www.freepik.com/free-ai-image/thunderstorm-countryside_274025040.htm">Image by freepik</a>
<a href="https://www.freepik.com/free-photo/beautiful-shot-green-plants-with-waterdrops-leaves-park-sunny-day_9853074.htm#fromView=search&page=1&position=1&uuid=d1c9fb9a-f6e3-4f60-9b6f-f0db72a7e5b9">Image by wirestock on Freepik</a>

<a href="https://www.freepik.com/free-vector/hand-drawn-tropical-leaves-background_13840082.htm#from_view=detail_alsolike">Image by freepik</a>
      

      
