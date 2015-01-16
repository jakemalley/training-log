# __init__.py
# Jake Malley
# 15/01/2015

"""
Creates the flask app.
"""

# Imports
from flask import Flask, render_template, abort

app = Flask(__name__)

# Define error handlers for HTTP errors.
@app.errorhandler(404)
def error_page_not_found(error):
    """
    When the page isn't found render the 404.html
    error page and display it to the user.
    """
    return render_template("404.html")

@app.errorhandler(500)
def error_page_not_found(error):
    """
    When the server encounters an error render 
    the 500.html error page and display it to the user.
    """
    return render_template("500.html")



