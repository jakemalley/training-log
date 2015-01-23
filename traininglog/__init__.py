# __init__.py
# Jake Malley
# 15/01/2015

"""
Creates the flask app.
"""

# Imports
from flask import Flask, render_template, abort
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Create the login manager.
login_manager = LoginManager()
login_manager.init_app(app)

# Define the route for logging in.
login_manager.login_view = "login.login"

# Make a database object.
db = SQLAlchemy(app)

# Import the error handlers.
import traininglog.error

# Import the blueprints.
from traininglog.login.views import login_blueprint
from traininglog.home.views import home_blueprint
from traininglog.dashboard.views import dashboard_blueprint

# Register the blueprints.
app.register_blueprint(login_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")

# Import the Member model.
from traininglog.models import Member

@login_manager.user_loader
def load_user(id):
    return Member.query.filter(Member.id == int(id)).first()