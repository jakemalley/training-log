# error.py
# Jake Malley
# 18/01/2015

"""
Defines error handlers for HTTP errors. Displays error.html
to the users with the error details.
"""

# Imports
from flask import render_template
# Import the app.
from traininglog import app

# Define error handlers for HTTP errors.
@app.errorhandler(401)
def error_page_not_found(error):
    """
    When the page isn't found render the error.html
    page and display it to the user with the 401 message.
    """

    # Create a dictionary with the error and error message.
    error_dictionary = dict(title="Unauthorised.", description="You need to login to view this page.", error_code=error)
    # Display the error page passing the error_dictionary.
    return render_template("error.html",error_dictionary=error_dictionary)

@app.errorhandler(403)
def error_page_not_found(error):
    """
    When the page isn't found render the error.html
    page and display it to the user with the 403 message.
    """

    # Create a dictionary with the error and error message.
    error_dictionary = dict(title="Forbidden.", description="You do not have the required permission to view that file.", error_code=error)
    # Display the error page passing the error_dictionary.
    return render_template("error.html",error_dictionary=error_dictionary)

@app.errorhandler(404)
def error_page_not_found(error):
    """
    When the page isn't found render the error.html
    page and display it to the user with the 404 message.
    """

    # Create a dictionary with the error and error message.
    error_dictionary = dict(title="Page not found.", description="The page you we're looking for couldn't be found.", error_code=error)
    # Display the error page passing the error_dictionary.
    return render_template("error.html",error_dictionary=error_dictionary)

@app.errorhandler(500)
def error_page_not_found(error):
    """
    When the page isn't found render the error.html
    page and display it to the user with the 500 message.
    """
    
    # Create a dictionary with the error and error message.
    error_dictionary = dict(title="Internal server error.", description="The server has encountered a server error.", error_code=error)
    # Display the error page passing the error_dictionary.
    return render_template("error.html",error_dictionary=error_dictionary)



