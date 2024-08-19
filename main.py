from app import flask_app

# Create app using flask_app function
app = flask_app()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)