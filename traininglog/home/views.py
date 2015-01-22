# home/views.py
# Jake Malley
# 22/01/15

"""
Define the routes for the home blueprint.
"""

from flask import flash, redirect, render_template, request, \
                    url_for, Blueprint

# Setup the home blueprint.
home_blueprint = Blueprint(
    'home',__name__,
    template_folder='templates'
    )

# Define the routes.
@home_blueprint.route('/')
def index():
    """
    If the user is logged in redirects to 
    the dashboard otherwise redirects to the 
    welcome page.
    """
    return redirect(url_for('home.welcome'))

@home_blueprint.route('/welcome')
def welcome():
    """
    Renders the welcome.html template and displays it the user.
    """

    return render_template('welcome.html')