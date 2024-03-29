# manage.py
# Jake Malley
# 15/01/2015

"""
Manage.py file uses Flask-Script to create a Manager
to allow us to run the app server and open a shell
inside the application context. It also provided the ability
to create custom commands. As well as perform database migrations.
"""

# Imports
from flask.ext.script import Manager,Server
from flask.ext.migrate import Migrate, MigrateCommand
from traininglog import app, db

# Create the manager object.
manager = Manager(app)
# Create the migration object. (For database migrations.)
migrate = Migrate(app, db)

# Get options for the server from the configuration.
try:
    # Get host from the configuration object.
    host = app.config['HOST']
except KeyError:
    # If the option isn't present use the default.
    host = '127.0.0.1'

try:
    # Get the port from the configuration object.
    port = app.config['PORT']
except KeyError:
    # If the option isn't present use the default.
    port=5000

# Create a development server to run the application.
server = Server(host=host, port=port)

# Specify custom commands for the manager.
@manager.command
def help():
    """
    Displays a simple help message. Instructing how to run the server.
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
    # Import all the models
    from traininglog.models import Member, Exercise, RunningLookUp, CyclingLookUp, SwimmingLookUp
    # Create the models.
    db.create_all()
    # Commit the changes.
    db.session.commit()

    # Generate the look up tables.
	# As per the data for caloried_burned per hour for someone 
	# of weight 80KG (Data given on the task sheet.)
    db.session.add(RunningLookUp(1, 472)) # 5 Mph (12 Minute mile)
    db.session.add(RunningLookUp(2, 590)) # 6 Mph (10 Minute mile)
    db.session.add(RunningLookUp(3, 679)) # 7 Mph (8.5 Minute mile)
    db.session.add(RunningLookUp(4, 797)) # 8 Mph (7.5 Minute mile)
    db.session.add(RunningLookUp(5, 885)) # 9 Mph (6.5 Minute mile)
    db.session.add(RunningLookUp(6, 944)) # 10 Mph (6 Minute mile)

    db.session.add(CyclingLookUp(1,236)) # <10 Mph, Leisure Cycling
    db.session.add(CyclingLookUp(2,354)) # 10-11.9 Mph, Gentle
    db.session.add(CyclingLookUp(3,472)) # 12-13.9 Mph, Moderate
    db.session.add(CyclingLookUp(4,590)) # 14-15.9 Mph, Vigorous
    db.session.add(CyclingLookUp(5,708)) # 16-20 Mph, Very Fast
    db.session.add(CyclingLookUp(6,944)) # >20 Mph, Racing

    db.session.add(SwimmingLookUp(1,413)) # Freestyle, Slow
    db.session.add(SwimmingLookUp(2,590)) # Freestyle, Fast
    db.session.add(SwimmingLookUp(3,413)) # Backstroke
    db.session.add(SwimmingLookUp(4,590)) # Breaststroke
    db.session.add(SwimmingLookUp(5,649)) # Butterfly

    # Commit the Changes.
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

# Add command for db migrations.
manager.add_command('db', MigrateCommand)
# Add the default runserver command for the application server
# we have specified.
manager.add_command('runserver', server)

# If it wasn't imported, but run directly.
if __name__ == "__main__":
    # Run the script manager.
    manager.run()