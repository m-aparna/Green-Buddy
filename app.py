from flask import Flask, render_template, request
from plant_basic_info import Plant_Basic_Info
from config import api_key

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('plant_info_homepage.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['plant_name']
        plant_info = Plant_Basic_Info(query, api_key)
        plant_basic_details = plant_info.basic_details()

        if plant_basic_details:
            return render_template('plant_basic_info.html', plant_basic_details=plant_basic_details)
        else:
            error_message = "Sorry, details were not found or an error occurred."
            return render_template('plant_basic_info.html', error = error_message)

    return render_template('plant_basic_info.html')

if __name__ == '__main__':
    app.run(debug=True)
