from flask import Flask

site = Flask(__name__)

from website import handler
