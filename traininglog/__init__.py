# __init__.py
# Jake Malley
# 15/01/2015

"""
Creates the flask app.
"""

# Imports
from flask import Flask, render_template, abort

app = Flask(__name__)

# Import the error handlers.
import traininglog.error