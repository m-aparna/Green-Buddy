# Contains all standard url endpoints related to user authentication
# Login, Sign Up, Dashboard

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Create a blueprint
auth = Blueprint('auth', __name__)

# Create a route for login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if username exists in db
        user = User.query.filter_by(email=email).first()
        if user: # If user exists
            # Check for valid password
            if check_password_hash(user.password, password): 
                flash('Logged in successfully', category='success')
                login_user(user, remember=True) # Login and remember the user
                return redirect(url_for('views.homepage')) 
            else:
                flash('Incorrect Password', category='error')
                return "Invalid credentials", 401
        else:
            flash('User doesn\'t exists. Please try again.', category='error')
            return "Invalid credentials", 401
    return render_template('login.html', user='')

# Create a route for logout page
@auth.route('/logout')
@login_required # Ensures that can only logout if user is already logged in
def logout():
    logout_user()
    return redirect(url_for('views.homepage'))

# Create a route for sign up page
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # Get data from form
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check if email already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists. Try logging in', category='error')
        elif password1 != password2:
            flash('Password does not match. Please try again', category='error')
        else:
            # Add user to db
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) # Login and remember the user
            # Flash a success message
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.homepage')) 
    return render_template('sign_up.html', user='')
