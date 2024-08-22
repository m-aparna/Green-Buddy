# 🌱 Green-Buddy- Your Home Gardening Buddy 👨‍🌾✂️🌳🍀
Group project -Group-1

## 📢 About The Project:
Green Buddy is a user-friendly website designed to help both registered and guest users perform gardening activities efficiently and effectively. With this app, users can create their own account to access information like detailed plant information,plant care tips,weather forecast details,nearby gardening shops,recommended videos based on plant to help plan their gardening activities effectively.

Green Buddy was created with an aim
to address the challenges
that many gardeners face
for not having proper information, such as choosing the right plants,understanding the care requirements, and managing their gardens effectively.
The website provides personalized recommendations, brief suggestions based on temperature, care guides,
and a platform where users can share their gardening experiences and advice.

### 🛠️ Problem Statement:

While gardening is an interesting hobby, but sometimes it is frustrating if things are not planned due to not having proper information.Some of the challenges faced by new gardeners are:

1. Lack of proper plant information: Many Gardeners don't have proper information about the plants.Lack of proper information about the plant results in poor planting.

2. Inadequate Plant Care: Due to lack of information and knowledge about plant care, gardeners especially new gardeners often struggle to take proper care for different types of plants. Care for plants often requires proper knowledge on areas like pruning,watering,sunlight requirements.This results in unhealthy plants and a bad gardening experience.

3. Adaptation to weather: Gardeners often struggle to get adapted to the rapidly changing weather conditions. Without proper information of weather conditions gardeners face poor planting experience which also damages their plants and affect the schedules of gardeners.

4. Limited Access to Quality Garden Shops: For gardeners it is important to get good quality of gardening supplies and advice on plants at local shops.Due to lack of time  and finding a good quality shop with proper rating,address where they can buy plants and other related items is challenging for gardeners.Not all garden shops offer a  range of products or knowledgeable staff, making it difficult for gardeners to find what they need.

5. User preference for visual information: Sometimes gardeners don't like to only read data. User prefers to visualise information through videos. Lack of proper information on good videos to follow may result in following bad suggestions.


### 💡 Solutions:

The goal of Green Buddy is to create a single platform that offers multiple services at one place, making it easier for gardeners, especially those who are new to gardening.The solutions provided by Green Buddy include:

1. Plant Information: When users enter the name of a plant, they receive detailed information about it, including how to grow and care for it.

2. Care Guides: Detailed care guides are available to help gardeners keep their plants healthy, covering everything from watering to pest control.

3. Garden Shop Locator: Users can find nearby gardening shops with information like ratings, addresses, and opening hours, making it easier to plan their visits and find what they need.

4. YouTube Recommendations: The platform suggests helpful YouTube videos on plant care, allowing gardeners to enhance gardening knowledge through easy-to-follow video tutorials.

5. Weather Forecast: A detailed current day along with 5-day weather forecast is provided,including alerts and suggestions based on the vegetative or flowering phase of plants considering temperature and humidity.

6. Plant Tracking: Users can add specific plants to their profile, including species information and other relevant details, allowing them to keep track of their plants and manage their care effectively.

### 🎨 Features:

Green Buddy enhances the gardening experience with the following features:

1. User Types:

- Guest Users: Access basic plant information without signing up. Guest users have limited functionality.

- Registered Users: Access additional features including personalized care guides, weather alerts, YouTube video suggestions, and nearby gardening shops. Registered users can also save notes.

2. Plant Information Search: Enter a plant name to get detailed information, including common and scientific names.

3. Plant Care Guides: Step-by-step guides for registered users on watering, feeding, pruning, and pest management.

4. Garden Shop Finder: Find nearby gardening shops with ratings, addresses, and opening hours.

5. YouTube Video Recommendations: Get suggestions for helpful plant care videos from trusted experts.

6. 5-Day Weather Forecast with Alerts: Receive a detailed 5-day weather forecast with alerts and suggestions based on your plants’ growth stages. Stay informed about sudden weather changes to protect your garden.

7. Plant Collections: Track your plants by adding and managing details like name, species, and care schedule. Option to add new plants or delete existing ones.

8. Signup Facility: Guest users can sign up to unlock personalized features and save their garden information.




## ✅ Tools/Technologies Used:

#### Backend:

- Flask Version 2.3.3

- Python 3.12.5 or higher

- SQLAlchemy 2.0.32

- pytest 8.3.2



#### Front end:

- Bootstrap
- HTML
- CSS

#### Front-end Template:

- Jinja2 Template


## 🌐 Important API and url used for the project:

- Weather API- https://openweathermap.org/api

   This is an open source API that offers real time weather data services for a current location.

       [api.openweathermap.org/data/2.5/forecast?q={city name}&appid={API key}&units=metric](WeatherAPI%20base%20url) : 
    
   This is the Base url used for fetching data from weather api.Add your API key and cityname to fetch weather data.


- Plant API - https://perenual.com/docs/api

   This open source API provides information about plants and their care guides.

- Youtube API-https://developers.google.com/youtube/v3


- Google places API - 

           https://developers.google.com/maps/documentation/places/web-service/text-search

   The Places API is a service that accepts HTTP requests for location and returns formatted data about establishments or prominent points of interest.

            https://places.googleapis.com/v1/places:searchText

   This url returns information about a set of places based on a string — for example "pizza in New York" 
   
   Pass all parameters in the JSON request body or in headers as part of the POST request. For example:
   
            curl -X POST -d '{
            "textQuery" : "Spicy Vegetarian Food in Sydney, Australia"
            }' \
            -H 'Content-Type: application/json' -H 'X-Goog-Api-Key: API_KEY' \
            -H 'X-Goog-FieldMask: places.displayName,places.formattedAddress,places.priceLevel' \
            'https://places.googleapis.com/v1/places:searchText'




- Google Maps embed- API-https://developers.google.com/maps/documentation/embed/get-started

   This is an open source API that offers Place an interactive map on web page.





## 🤔 How to Run

### Setup

1. #### Install Python 3.12.5 or Higher

    - Download the latest version of Python from python.org.
    - Ensure Python is added to your PATH (for Windows users).
    - Note: Python 3.12.4 was used during the development of this project.

2. #### Create a Virtual Environment

    - It’s advisable to run this project inside a virtual environment to avoid conflicts with your system’s dependencies.

    - Windows (Command Prompt):

          cd Green-Buddy
          pip install virtualenv
          python3 -m virtualenv venv
   
      or

          python3 -m venv venv

   - macOS/Linux:

         cd Green-Buddy
         pip install virtualenv
         python -m virtualenv venv

3. #### Activate the Virtual Environment

   - Windows (Command Prompt):

         venv\scripts\activate

   - macOS/Linux:
   
         . venv/bin/activate
   
   or

          source venv/bin/activate


4. #### Install the Requirements

   - Install all required packages by running:
   

        pip install -r requirements.txt

5. #### Set Up SQLAlchemy

   - Update the project with your SQLAlchemy  credentials by replacing the username, password, and database_name placeholders.

   
6. #### Install Required Modules, Libraries, and Packages

   - Follow the instructions in the [Modules/Packages/library](Modules/Packages/library) section to install all necessary dependencies.

7. #### Clone the Repository

    - Clone the project repository:

        
       git clone https://github.com/github_username/repo_name.git

8. #### Navigate to the Project Directory

    - Move into the project directory:

       
         cd Green-Buddy

9. #### Configure APIs and Keys

     - Create accounts on the required API platforms mentioned in the [Important API Used for the Project](Important API used for the project) section.

     - Obtain the necessary API keys and replace the placeholders in config.py with your actual API keys.

     - Example:

           API_KEY = 'YOUR_API_KEY'

     - Set a secret key for Flask (e.g., "my_secret_key").

   
10. #### Run the Flask Application

      - Start the application by running:

             python main.py
    
      - The application will be accessible at http://127.0.0.1:5000.
    

#### 🏠 Homepage Options:

Once on the homepage, you’ll see three user options:

   - Guest User:
    
      Access basic features, such as plant information, without signing up.Simply enter a plant name to get detailed information.

   - Signup:

     New users can create an account to access additional features available to registered users.

   - Login:

     Registered users can log in to access the full range of Green Buddy’s features.

#### 🧭  Navigating Features:

- Registered Users:

   Once logged in, registered users can access various features, such as:

     - Plant Care: Enter a plant name to receive comprehensive care details.
  
     - Weather Details: View detailed weather information.
  
     - Nearby Shops: Locate gardening shops.
  
     - Plant Management: Add and manage your plants.
  
#### 🧭 Logout:

   After using the website, you can log out by clicking the "Logout" option located at the top right corner of the page.







## 🚀 Modules/Packages/library:

- Requests : This module allows sending HTTP  requests using python

            pip install requests



- Collections: It is a built-in module,there is no need to install it.The collection Module in Python provides different types of containers. A Container is an object that is used to store different objects and provide a way to access the contained objects and iterate over them. 

In this project we have used Counter().

Counter() -A counter is a sub-class of the dictionary.It is used to keep the count of the elements in an iterable in the form of an unordered dictionary where the key represents the element in the iterable and value represents the count of that element in the iterable.
    
            from collections import Counter

            

- flask: A WSGI web application framework for Python.  It is used to build websites using python and handles requests from users easily.

            pip install flask

- Flask login  : Flask-Login provides user session management for Flask.It handles the common tasks of logging in, logging out, and remembering your users' sessions over extended periods of time.
      
          pip install flask-login

- Flask SQLAlchemy: Flask-SQLAlchemy is an extension for Flask.It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.

      pip install flask-sqlalchemy


- Google API client (YouTube API) :------------------------------------

      pip install google-api-python-client

-  Jinja2 template/render_templates : A template is rendered with specific data to produce a final document. Flask uses the Jinja template library to render templates.We will use templates to render HTML which will display in the user’s browser.

No need to install it. It needs to be imported from flask.



## 📂 File Structure/Project Directory:


![img_3.png](img_3.png)




-----------------


## 🌐 API Endpoints or API used:

GET- The methods (methods=['GET']) is a keyword argument that lets Flask know what kind of requests it is.This method is used to retrieve data from the server.

POST- This method enables users to send data over to the server

Endpoint: http://127.0.0.1:5000/Auth
Method type:
Details: -----------------------------------

Endpoint: http://127.0.0.1:5000/weather
Method Type: POST
Details: Provides users with detailed weather information, including a 5-day forecast, alerts, and gardening suggestions based on current and upcoming weather conditions.


Endpoint: http://127.0.0.1:5000/shops 
Method Type: POST 
Details: Helps users find gardening shops that are close to their current location, along with relevant details such as ratings, addresses, and opening hours. Which helps user to  plan their visits and get the supplies they need without traveling far.


## 🔍 Future Enhancements:

We plan to introduce the following enhancements in future updates:

   - Automatic Notifications: Reminders for watering, pruning, and other tasks.

## 🤝Contributions
This project was a collaborative effort with significant contributions from:

- **Akhila Kukkadala -**  
    Lead Developer, Backend Specialist,API Integration

    GitHub: [akhila3894](https://github.com/akhila3894)


- **Aparna Mishra-**  

    Lead Developer, Backend Specialist,API Integration

    GitHub:[m-aparna](https://github.com/m-aparna)


- **Ashwini Ravikumar-**  
      UI/UX Designer,Database Management
      GitHub:https://github.com/Ashie-03


  
## 📚Resources


- SQLAlchemy Documentation:  https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/


- Flask Documentation: https://flask.palletsprojects.com/en/3.0.x/


- Flask Jinja2 Template Documentation:  https://flask.palletsprojects.com/en/3.0.x/


- Flask-Login:   https://flask.palletsprojects.com/en/3.0.x/


- Bootstrap Documentation: https://getbootstrap.com/docs/5.3/getting-started/introduction/

- Pytest: https://docs.pytest.org/en/stable/


- Collection Module - https://docs.python.org/3/library/collections.html


- OpenWeatherMap API:  https://openweathermap.org/api


- Perenual Plant API: 


- YouTube API: 


- Google Places API:  https://developers.google.com/maps/documentation/places/web-service/text-search


- Google Maps Embed  API : https://developers.google.com/maps/documentation/embed/get-started


## 🖼️ Image Attributions:
Special thanks to the creators of the images used in this project:

Plant Care background image- <a href="https://www.freepik.com/free-photo/top-view-plants-frame_13560941.htm#fromView=search&page=1&position=15&uuid=e73990df-f33d-40f1-b1ed-3009e760338c">Image by freepik</a>

Weather background image-  <a href="https://www.freepik.com/free-photo/macro-shot-water-droplets-leaves-green-plant_17116047.htm#from_view=detail_alsolike">Image by wirestock on Freepik</a>

Dashboard background - <a href="https://www.freepik.com/free-vector/tropical-flower-background_2920876.htm#from_view=detail_alsolike">Image by pikisuperstar on Freepik</a>

Places API service image - <a href="https://www.freepik.com/free-vector/flower-shop-facade-night-city-street-vector-cartoon-illustration-urban-floral-boutique-gift-storefront-with-illuminated-windows-garlands-striped-tent-door-flowerpots-shelf_66811049.htm#fromView=search&page=2&position=48&uuid=48f47d53-7e5d-48c4-a563-969639b77082">Image by upklyak on Freepik</a>

Add plant service image - <a href="https://www.freepik.com/free-vector/hand-drawn-people-taking-photos-with-smartphone_16408153.htm#fromView=search&page=1&position=3&uuid=9e29063a-d810-4a0f-8923-ec6a9ea23d97">Image by pikisuperstar on Freepik</a>

Plant Care background image- <a href="https://www.freepik.com/free-photo/top-view-plants-frame_13560941.htm#fromView=search&page=1&position=15&uuid=e73990df-f33d-40f1-b1ed-3009e760338c">Image by freepik</a>


## 💬 Conclusion:


Green Buddy is an all-in-one platform designed to enhance the gardening experience, especially for new gardeners. It offers easy access to plant information, care guides, weather forecasts, and nearby garden shop locators, all in one place. The user-friendly interface ensures that both guest and registered users can quickly find the resources they need. With personalized recommendations and YouTube video suggestions, Green Buddy supports gardeners at every step, helping them make informed decisions and keep their plants thriving. Whether you're starting your first garden or managing a larger one, Green Buddy is your trusted companion on this green journey.Happy Planting!
!!!!! 🌱

