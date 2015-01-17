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

    # Create a dictionary with the error and error message.
    error_dictionary = dict(title="Page not found.", description="The page you we're looking for couldn't be found.", error_code=error)
    # Display the error page passing the error_dictionary.
    return render_template("error.html",error_dictionary=error_dictionary)

@app.errorhandler(500)
def error_page_not_found(error):
    """
    When the server encounters an error render 
    the 500.html error page and display it to the user.
    """
    
    # Create a dictionary with the error and error message.
    error_dictionary = dict(title="Internal server error.", description="The server has encountered a server error.", error_code=error)
    # Display the error page passing the error_dictionary.
    return render_template("error.html",error_dictionary=error_dictionary)



