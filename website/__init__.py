# Import flask
from flask import Flask

# Setup CSRF Protection for Login/Signup Form Validation
from flask.ext.wtf import CSRFProtect

# Setup mail for website
from flask.ext.mail import Mail

# Create the flask site
site = Flask(__name__)
# Create/Initalize the CSRF Protection on site
csrf = CSRFProtect()
csrf.init_app(site)

# Create a mail manager for the site
from Mail import MailManager
mail = MailManager(site)

from website import handler
