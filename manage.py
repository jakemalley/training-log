# manage.py
# Jake Malley
# 15/01/2015

"""
Manage file uses Flask-Script to create a Manager
to allow us to run the app server and open a shell
inside the application context.
"""

# Imports
from flask.ext.script import Manager
from traininglog import app
from os import environ

# Get the configuration class to use from a environment variable.
try:
    app.config.from_object(environ['TRAINING_LOG_CONFIG'])
except KeyError:
    # The environment variable was not set.
    # Assume we're in production.
    app.config.from_object('config.ProductionConfig')
else:
    # If we could get the config from the environment variable print it out.
    print(environ['TRAINING_LOG_CONFIG'])


manager = Manager(app)

if __name__ == "__main__":

    manager.run()