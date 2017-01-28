# Import flask
from flask import Flask

# Setup CSRF Protection for Login/Signup Form Validation
from flask.ext.wtf import CSRFProtect

# Create the flask site
site = Flask(__name__)
# Create/Initalize the CSRF Protection on site
csrf = CSRFProtect()
csrf.init_app(site)

from website import handler
