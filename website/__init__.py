# Import flask lib object
from flask import Flask
# Import flask login objects
from flask.ext.login import LoginManager

# Setup the site & login manager
site = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(site)

from website import handler
