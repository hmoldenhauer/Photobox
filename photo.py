import RPi.GPIO as GPIO
from sh import gphoto2 as gp
import os
from pynput.keyboard import Listener
import datetime as dtime
import sqlite3 as sq

from configuration import *

# Status LED
# These Leds will glow, when a image is processed
RedLedPin_1 = 7
RedLedPin_2 = 11
RedLedPin_3 = 13
RedLedPin_4 = 16

# This Led will glow, when the photobox is ready to take an image
GreenLedPin = 12

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(RedLedPin_1, GPIO.OUT)    # input mode
    GPIO.setup(RedLedPin_2, GPIO.OUT)    #
    GPIO.setup(RedLedPin_3, GPIO.OUT)    #
    GPIO.setup(RedLedPin_4, GPIO.OUT)    #
    GPIO.setup(GreenLedPin, GPIO.OUT)    #

    # Turn off the Red Leds and turn on the green Led
    GPIO.output(RedLedPin_1, False)
    GPIO.output(RedLedPin_2, False)
    GPIO.output(RedLedPin_3, False)
    GPIO.output(RedLedPin_4, False)
    GPIO.output(GreenLedPin, True)


def take_a_photo():
    # Set LEDs to 'Photo is processed'
    GPIO.output(RedLedPin_1, True)
    GPIO.output(RedLedPin_2, True)
    GPIO.output(RedLedPin_3, True)
    GPIO.output(RedLedPin_4, True)
    GPIO.output(GreenLedPin, False)

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
    ############### The os.rename is needed if you use a Sony Alpha 6000 ################################################################################

    os.rename( 'capt0000.jpg', 'photobox_' + str(int(max_file_number)).zfill(4) + '.jpg') #rename file
    f = open(homefolder + '/stats_dats/max_file_number.txt', 'w')
    f.write('%i' % max_file_number)
    f.close()

    # save photo_number and a timestamp to the db

    image_numberCursor.execute("""INSERT INTO image_taken VALUES({}, "{}")""".format(max_file_number,dtime.datetime.now().time().strftime("%H:%M")) )

    ###################################################################################################################################


    ################ For the Canon camera I have to define an offest ##################################################################
    # It is not used in this script. I just inserted here as a reminder.
    # The output of some cameras does not start at zero.
    canon_offset = 7000

    # save photo_number and a timestamp to the db
    image_numberCursor.execute("""INSERT INTO image_taken VALUES({}, "{}")""".format(max_file_number,dtime.datetime.now().time().strftime("%H:%M")) )
    ###################################################################################################################################

    # conncetion_number_log is a global variable
    connection_number_log.commit()

    # Set Leds to 'Ready for photo'
    GPIO.output(RedLedPin_1, False)
    GPIO.output(RedLedPin_2, False)
    GPIO.output(RedLedPin_3, False)
    GPIO.output(RedLedPin_4, False)
    GPIO.output(GreenLedPin, True)

    print('Done')


# Function used to clear GPIO pins and close db connection after usage
def destroy():
    GPIO.cleanup()
    connection_number_log.close()


# Function which detects the input key of the presenter
def on_press(key):
    # "u'.'" was sended by the presenter when the middle button was pressed
    if str(key) == photo_key:
        take_a_photo()
        #print(str(key))
    elif str(key) == stop_key:
        Listener.stop()
        destroy()
    else:
        print('nichts')
        pass


# Hard coded path to save media
# in this case I used a usb_stick
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


# Let's take some images!!
setup()
while True:

    try:
        # Listener reads the input over keyboard or presenter
        # on_press is the function which is called when the pi gets an input
        # via keyboard or presenter
        with Listener(on_press=on_press,) as listener:
            listener.join()
    except KeyboardInterrupt:
        destroy()
