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

manager = Manager(app)
migrate = Migrate(app, db)

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

# Create a development server to run the application.
server = Server(host=host, port=port)

# Specify custom commands
@manager.command
def help():
    """
    Displays a simple help message.
    """
    print("""
    To run the development server use $ python manage.py runserver
    To run the production server use $ python manage.py tornadoserver
        """)
    
@manager.command
def init_db():
    """
    Create a new database as per the models specified
    in the models.py file. Using the database file specified
    in the config.py
    """
    from traininglog.models import Member
    db.create_all()
    db.session.commit()

@manager.command
def tornadoserver():
    """
    Create a tornado server to run the application 
    (used in production).
    """
    # Import tornado for our tornado server.
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    # Import signal used to stop tornado with ctrl-c.
    import signal

    # Define a callback to stop the server.
    def stop_tornado(signum, frame):
        # Stop the loop.
        IOLoop.instance().stop()

    signal.signal(signal.SIGINT, stop_tornado)
    # Create the HTTP server and WSGI Container.
    http_server = HTTPServer(WSGIContainer(app))
    # Listen on the port specified in the config.
    http_server.listen(port)
    # Start the loop.
    IOLoop.instance().start()

# Add commands to the manager.
# Add command for db migrations.
manager.add_command('db', MigrateCommand)
# Add the default runserver command for the application server.
manager.add_command('runserver', server)

if __name__ == "__main__":
    # Run the script manager.
    manager.run()