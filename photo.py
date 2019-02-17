import RPi.GPIO as GPIO
from sh import gphoto2 as gp
import os
from pynput.keyboard import Listener
import datetime as dtime
import sqlite3 as sq

from configuration import *

def take_a_photo():
    # Try to get the last photo number
    try:
        image_numberCursor.execute(""" SELECT max(Image_Number) FROM image_taken""")
        # max_file_number is the number of the latest photo
        max_file_number = image_numberCursor.fetchall()[0][0]
    # If there is not db named "image_taken", we create one
    except sq.OperationalError:
        image_numberCursor.execute(""" CREATE TABLE image_taken(Image_Number SMALLINT ,Time_Stampt TEXT)""")
        connection_number_log.commit()
        # Set max_file_number to zero (no images)
        max_file_number = 0
        pass

    # we take a new photo, so we have to increase the number of max_photos
    max_file_number += 1
    print('taking')
    # takeing a photo
    gp( '--capture-image-and-download' )

    # rename file, this depends on your camera !
    os.rename( 'capt0000.jpg', 'photobox_' + str(int(max_file_number)).zfill(4) + '.jpg') #rename file
    bashCommand = 'convert -geometry ' + str(int(int(image_width)/2)) + 'x' + str(int(int(image_height)/2)) + \
                  ' -quality 90 ' + 'photobox_' + str(int(max_file_number)).zfill(4) + '.jpg' +\
                  ' photobox_small_' + str(int(max_file_number)).zfill(4) + '.jpg'
    print(bashCommand)
    os.system(bashCommand)

    f = open(homefolder + '/stats_dats/max_file_number.txt', 'w')
    f.write('%i' % max_file_number)
    f.close()

    # save photo_number and a timestamp to the db
    image_numberCursor.execute("""INSERT INTO image_taken VALUES({}, "{}")""".format(max_file_number,dtime.datetime.now().time().strftime("%H:%M")) )

    # conncetion_number_log is a global variable
    connection_number_log.commit()

    print('Done')


# Function used to clear GPIO pins and close db connection after usage
def destroy():
    connection_number_log.close()


# Function which detects the input key of the presenter
def on_press(key):
    if str(key) == photo_key:
        take_a_photo()
    elif str(key) == stop_key:
        Listener.stop()
        destroy()
    else:
        print('nichts')
        pass


# path to save media
os.chdir(imagefolder)

# Hard coded global variables
global connection_number_log
global image_numberCursor

# connection to the db which includes the max_number of image taken
# check_same_thread=True enables the possibility to read/write
# the db with more than one program
connection_number_log = sq.connect(homefolder + '/stats_dats/image_taken.dat',
                                   check_same_thread=False)
image_numberCursor = connection_number_log.cursor()

print('Photobox running')
gp('--set-config', 'autofocus=0')


# Let's take some images!!
while True:

    try:
        # Listener reads the input over keyboard or presenter
        # on_press is the function which is called when the pi gets an input
        # via keyboard or presenter
        with Listener(on_press=on_press,) as listener:
            listener.join()
    except KeyboardInterrupt:
        destroy()
