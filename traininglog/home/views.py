# home/views.py
# Jake Malley
# 22/01/15

"""
Define the routes for the home blueprint.
"""

# Imports.
from flask import redirect, render_template, url_for, Blueprint
from traininglog.login.forms import LoginForm
from flask.ext.login import current_user

# Setup the home blueprint.
home_blueprint = Blueprint(
    'home',__name__,
    template_folder='templates'
    )

# Define the routes.
@home_blueprint.route('/')
@home_blueprint.route('/None') # Added /None as when there is a redirect error using request.referrer
def index():
    """
    If the user is logged in redirects to 
    the dashboard otherwise redirects to the 
    welcome page.
    """
    # If the user is logged in.
    if current_user.is_authenticated():
        # Redirect to the dashboard.
        return redirect(url_for('dashboard.dashboard'))
    else:
        # Redirect to the welcome page.
        return redirect(url_for('home.welcome'))

@home_blueprint.route('/welcome')
def welcome():
    """
    Renders the welcome.html template and displays it the user.
    """
    if current_user.is_authenticated():
        # Redirect to the dashboard.
        return redirect(url_for('dashboard.dashboard'))
    else:
        # Render the welcome page passing in the login form.
        return render_template('home_welcome.html',user_login_form=LoginForm())