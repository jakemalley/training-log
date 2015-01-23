# manage.py
# Jake Malley
# 15/01/2015

"""
Manage file uses Flask-Script to create a Manager
to allow us to run the app server and open a shell
inside the application context.
"""

# Imports
from flask.ext.script import Manager,Server
from flask.ext.migrate import Migrate, MigrateCommand
from traininglog import app
from traininglog import db
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

@manager.command
def init_db():
    from traininglog.models import Member
    db.create_all()
    db.session.commit()

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# Get options from the config.
try:
    # Get host from the config.
    host = app.config['HOST']
except KeyError:
    # If the option isn't present use the default.
    host = '127.0.0.1'

try:
    # Get the port from the config.
    port = app.config['PORT']
except KeyError:
    # If the option isn't present use the default.
    port=5000

# Create the server to run the application.
server = Server(host=host, port=port)

# Add commands to the manager.
# Add the default runserver command for the application server.
manager.add_command('runserver', server)

if __name__ == "__main__":

    manager.run()