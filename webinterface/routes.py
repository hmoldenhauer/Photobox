# coding: utf-8
import flask
from webinterface import app
from flask_socketio import SocketIO
import threading
import numpy as np
import sqlite3 as sq

socketio = SocketIO(app)
connection_number_log = sq.connect('/home/pi/rasberry/party_photobox/stats_dats/image_taken.dat',check_same_thread=False)
image_numberCursor = connection_number_log.cursor()


@app.before_first_request
def init_app():
    start_image_updater()


def start_image_updater():
    #Update
     t = threading.Timer(1.5, start_image_updater)
     t.daemon = True
     t.start()
     #Get the number of the newest photo
     image_numberCursor.execute(""" SELECT max(Image_Number) FROM image_taken""")

    
    
     photo_number = image_numberCursor.fetchall()[0][0]
     print(photo_number)

     ### In further updates I will use an argument for this ###

     ####### For the Sony Alpha 6000 #####################################################
     # Generate the name for the html template. I was not sure how to use a variable in "url_for", so I trie this as workaround

     #pic_name = "/photo_folder/photobox_" + str(int(photo_number)) + ".jpg"
     #################################################################################################################

    ####### For the Canon camera #####################################################
     # Generate the name for the html template. I was not sure how to use a variable in "url_for", so I trie this as workaround
     canon_offset = 7021
     pic_name = "/photo_folder/IMG_" + str(int(photo_number+canon_offset)) + ".JPG"
     ################################################################################################################

     print(pic_name)
     emit_var = [ 'Bildnummer: ' + str(int(photo_number)), pic_name ]
     #Emit Update command
     socket.emit('update', emit_var)
     #socket.emit('title_update', str(int(photo_number)))



### Init socket
socket = SocketIO()
socket.init_app(app)


# The first apparance of the website is defined here. So it should show at the beginning the image with number 1
@app.route('/')
def test():
    image_name = 'image_1.jpg'
    image_number = '1'
    return flask.render_template('show_picture.html', image_name = image_name, image_number = image_number)

# Just a test function
@app.route('/test')
def test_2():
    return 'Geklappt'
