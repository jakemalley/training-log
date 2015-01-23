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

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Make a database object.
db = SQLAlchemy(app)

# Import the error handlers.
import traininglog.error

# Import the blueprints.
from traininglog.login.views import login_blueprint
from traininglog.home.views import home_blueprint

# Register the blueprints.
app.register_blueprint(login_blueprint)
app.register_blueprint(home_blueprint)