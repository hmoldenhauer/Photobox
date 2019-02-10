# coding: utf-8
from flask import Flask

from configuration import *

# Start Flask app
app = Flask(__name__,static_folder="/home/pi/Pictures")
app.config['SECRET_KEY'] = "DuWeißtSchonWer"

from webinterface import routes
