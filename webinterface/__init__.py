# coding: utf-8
from flask import Flask

app = Flask(__name__,static_folder="/media/pi/Marten/photo_folder")
app.config['SECRET_KEY'] = "DuWeißtSchonWer"

from webinterface import routes