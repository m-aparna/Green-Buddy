from app import create_app

db_name = 'User.db'
db_URI = f'sqlite:///{db_name}'
# Create app using flask_app function
app = create_app(db_URI)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
