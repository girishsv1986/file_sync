# Import flask and template operators
from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Define the WSGI application object
FLASK_APP = Flask(__name__)

# Configurations
FLASK_APP.config.from_object('config')

# Define the database object which is imported
DB = SQLAlchemy(FLASK_APP, session_options={'autocommit': True})
MA = Marshmallow(FLASK_APP)

from file_sync.controllers.file import file_routes

# Register blueprint(s)
FLASK_APP.register_blueprint(file_routes)

# Build the database:
# This will create the database file using SQLAlchemy
DB.create_all()
