# coding: utf-8
import flask
from webinterface import app
from flask_socketio import SocketIO
import threading
import numpy as np
import sqlite3 as sq
import re

from configuration import *

# the socket gives the opportunity to update the website
socketio = SocketIO(app)
# Connet to db which included the max number of images
connection_number_log = sq.connect(homefolder + '/stats_dats/image_taken.dat', check_same_thread=False)
image_numberCursor = connection_number_log.cursor()


# before we create the webinterface,
# the start_image_updater function is called
@app.before_first_request
def init_app():
    start_image_updater()

def start_image_updater():
    # Everysecond we call the funtion start_image_updater
    # That means that every 1.5 seconds we update the webside and check
    # latest photo_number
    t = threading.Timer(1.5, start_image_updater)
    # Daemon threads are useful for background supporting tasks
    # such as garbage collection, releasing memory of unused
    # objects and removing unwanted entries from the cache.
    # More information: https://www.baeldung.com/java-daemon-thread
    t.daemon = True
    # Start timer
    t.start()
    # Get the number of the newest photo
    image_numberCursor.execute(""" SELECT max(Image_Number) FROM image_taken""")
    photo_number = image_numberCursor.fetchall()[0][0]

   
    # Generate the name for the html template. I was not sure how to use a variable in "url_for", so I trie this as workaround
    lastfolder = re.findall('([^\/]+$)', imagefolder)[0]
    pic_name = "/" + lastfolder + "/photobox_" + str(int(photo_number)).zfill(4) + ".jpg"

    emit_var = ['Bildnummer: ' + str(int(photo_number)), pic_name]
    socket.emit('update', emit_var)
    
# Init socket
socket = SocketIO()
socket.init_app(app)

# The first appearance of the website is defined here.
# So it should show at the beginning the image with number 1
@app.route('/')
# I should change the name of this function
def test():
    image_name = 'photobox_1.jpg'
    image_number = '1'
    return flask.render_template('show_picture.html', image_name = image_name,
                                                      image_number = image_number,
                                                      image_height = image_height,
                                                      image_width = image_width,
                                                      bg_color = bg_color,
                                                      font_color = font_color)
