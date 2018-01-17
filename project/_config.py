# holds the app's settings and configuration global variables
import os

# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG=False

DATABASE = "flasktaskr.db"
# is used for cross-site request forgery prevention (app goes more secure)
CSRF_ENABLED = True
SECRET_KEY = "je|zUn@B6vYC4x&dl`_?uM|cEWp;'S"

# define the full path for the DATABASE
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the DATABASE uri
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False
