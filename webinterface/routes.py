# coding: utf-8
import flask
from webinterface import app
from flask_socketio import SocketIO
import threading
import numpy as np
import sqlite3 as sq

# the socket gives the opportunity to update the website
socketio = SocketIO(app)
# Connet to db which included the max number of images
connection_number_log = sq.connect('/home/pi/rasberry/party_photobox/stats_dats/image_taken.dat', check_same_thread=False)
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
    print(photo_number)

    ### In further updates I will use an argument for this ###

    ####### For the Sony Alpha 6000 #####################################################
    # Generate the name for the html template. I was not sure how to use a variable in "url_for", so I trie this as workaround

    #pic_name = "/photo_folder/photobox_" + str(int(photo_number)) + ".jpg"
    #################################################################################################################

    ###### For the Canon camera #####################################################
    # Generate the name for the html template. I was not sure how to use a variable in "url_for", so I trie this as workaround
    # I have take the offset into account, because
    # now I load the image from the image folder
    # There are two possibilities to handle the offset:
    # 1. add the offset when max_image_number is saved to the db
    # 2. add the offset when you load the image (chosen here)
    canon_offset = 7021
    pic_name = "/photo_folder/IMG_" + str(int(photo_number+canon_offset)) + ".JPG"
    ################################################################################################################

    print(pic_name)
    # title for the .html
    emit_var = ['Bildnummer: ' + str(int(photo_number)), pic_name]
    # Emit Update command
    socket.emit('update', emit_var)
    # socket.emit('title_update', str(int(photo_number)))


# Init socket
socket = SocketIO()
socket.init_app(app)


# The first appearance of the website is defined here.
# So it should show at the beginning the image with number 1
@app.route('/')
# I should change the name of this function
def test():
    image_name = 'image_1.jpg'
    image_number = '1'
    return flask.render_template('show_picture.html', image_name = image_name, image_number = image_number)

# Just a test function
@app.route('/test')
def test_2():
    return 'Geklappt'
