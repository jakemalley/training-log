# config.py
# Jake Malley
# 15/01/2015

# Imports
import os

"""
Defines a default configuration class DefaultConfig
and classes for production and development configuration: 
ProductionConfig and DevelopmentConfig respectively.
"""

class DefaultConfig(object):
    """
    Default configuration settings. All other
    configuration class should inherit from this class.
    """

    # Disables debugging by default.
    DEBUG = False
    # Specify a secret key. (Will be different in production.)
    SECRET_KEY = '\t\x0b\xcf\xa3Fpj\x18\x04\x83\xb5\x0b\xe7\xa2\x0c\x12\x04B\x0c\x87\xfeLkS'
    # SQLite Database.
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.abspath("training_log_database.db")
    
    # Options for member sign up.
    # Automatically approve users when they sign up.
    AUTO_APPROVE = True
    # Automatically make users administrators when they sign up.
    AUTO_ADMIN = False

class DevelopmentConfig(DefaultConfig):
    """
    Configuration to be used in development environments only!
    (Don't test your code in production with this configuration!)
    """

    # Warn the user so they know they're using the development configuration when running the server.
    print(" * Warning using development configuration.")

    # Enables debugging in development environments
    DEBUG = True

class ProductionConfig(DefaultConfig):
    """
    Configuration to be used in production environments.
    """

    # Explicitly make sure debugging is disabled.
    DEBUG = False
    
    # SQLite Database.
    #SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.abspath("training_log_database.db")
    # Specify a absolute path for SQLite in /tmp (Needed when running with uWSGI)
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/training_log_database.db"

    # Set the host and port.
	# (Only used when running the app via manage.py)
    HOST = '0.0.0.0'
    PORT = 8080