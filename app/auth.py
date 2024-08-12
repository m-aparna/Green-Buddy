# Contains all standard url endpoints related to user authentication
# Login, Sign Up, Dashboard

from flask import Blueprint, render_template, request, flash, redirect, url_for

# Create a blueprint
auth = Blueprint('auth', __name__)

# Create a route for login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

# Create a route for logout page
@auth.route('/logout')
def logout():
    return render_template('#') # Add template here

# Create a route for sign up page
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    # Get data from form
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Validate email too in the if statements
        if password1 != password2:
            flash('Password does not match. Please try again', category='error')
        else:
            # Add user to db
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.homepage')) # Should redirect to dashboard
    return render_template('sign_up.html')
