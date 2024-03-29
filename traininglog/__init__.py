# __init__.py
# Jake Malley
# 15/01/2015

"""
Tells python to treat this directory as a package.
Creates the flask app. 
"""

# Imports
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from os import environ

# Create the flask app.
app = Flask(__name__)
# Create a bcrypt object for password hashing.
bcrypt = Bcrypt(app)

# Get the configuration class to use from a environment variable.
try:
    # Load the configuration class specified in the environment variable
    # 'TRAINING_LOG_CONFIG'
    app.config.from_object(environ['TRAINING_LOG_CONFIG'])
except KeyError:
    # The environment variable was not set.
    # Assume we're in production (Use ProductionConfig class).
    app.config.from_object('config.ProductionConfig')

# Create the login manager.
login_manager = LoginManager()
# Initialize login_manager.
login_manager.init_app(app)

# Define the route for logging in.
login_manager.login_view = "login.login"
# Define the route for refreshing login.
login_manager.refresh_view = "login.login"
# Message flashed when logging in.
login_manager.needs_refresh_message = (
    u"To protect your account, please re authenticate to access this page."
)

# Make a database object. (Using the URI in the configuration.)
db = SQLAlchemy(app)

# Import the error handlers.
import traininglog.error

# Import the blueprints.
from traininglog.login.views import login_blueprint
from traininglog.home.views import home_blueprint
from traininglog.dashboard.views import dashboard_blueprint
from traininglog.exercise.views import exercise_blueprint
from traininglog.weight.views import weight_blueprint
from traininglog.admin.views import admin_blueprint

# Register the blueprints.
app.register_blueprint(login_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")
app.register_blueprint(exercise_blueprint, url_prefix="/exercise")
app.register_blueprint(weight_blueprint, url_prefix="/weight")
app.register_blueprint(admin_blueprint, url_prefix="/admin")

# Import the Member model.
from traininglog.models import Member

@login_manager.user_loader
def load_user(id):
    # Load (and return) the member object with the given member id = id.
    return Member.query.filter(Member.id == int(id)).first()