import time
import RPi.GPIO as GPIO
from sh import gphoto2 as gp
import os
from pynput.keyboard import Listener
import datetime as dtime
import sqlite3 as sq

#Status LED
RedLedPin_1 = 7 # This Led will glow, when we are ready to take a photo
RedLedPin_2 = 11 # This Led will glow, when we are ready to take a photo
RedLedPin_3 = 13 # This Led will glow, when we are ready to take a photo
RedLedPin_4 = 16 # This Led will glow, when we are ready to take a photo
GreenLedPin = 12 # This Led will glow, when we are ready to take a photo




def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(RedLedPin_1, GPIO.OUT)    # input mode
    GPIO.setup(RedLedPin_2, GPIO.OUT)    #
    GPIO.setup(RedLedPin_3, GPIO.OUT)    #
    GPIO.setup(RedLedPin_4, GPIO.OUT)    #
    GPIO.setup(GreenLedPin, GPIO.OUT)    # 
    
    GPIO.output(RedLedPin_1, False)
    GPIO.output(RedLedPin_2, False)
    GPIO.output(RedLedPin_3, False)
    GPIO.output(RedLedPin_4, False)
    GPIO.output(GreenLedPin,True)
    return 0


def take_a_photo():
    GPIO.output(RedLedPin_1, True)
    GPIO.output(RedLedPin_2, True)
    GPIO.output(RedLedPin_3, True)
    GPIO.output(RedLedPin_4, True)
    GPIO.output(GreenLedPin,False)

    try: 
        image_numberCursor.execute(""" SELECT max(Image_Number) FROM image_taken""")
        max_file_number = image_numberCursor.fetchall()[0][0]
    except sq.OperationalError:
        image_numberCursor.execute(""" CREATE TABLE image_taken(Image_Number SMALLINT ,Time_Stampt TEXT)""")
        connection_number_log.commit()
        max_file_number = 0
        pass
       
    max_file_number += 1
    print('taking_2')
    gp( '--capture-image-and-download' ) #takeing a photo
    print('downloaded')

    ############### The os.rename is needed if you use a Sony Alpha 6000 ################################################################################

    #os.rename( 'capt0000.jpg', 'photobox_' + str(int(max_file_number)) + '.jpg') #rename file
    #image_numberCursor.execute("""INSERT INTO image_taken VALUES({}, "{}")""".format(max_file_number,dtime.datetime.now().time().strftime("%H:%M")) )

    ###################################################################################################################################


    ################ For the Canon camera I have to define an offest ##################################################################
    canon_offset = 7000 # It is not used in this script. I just inserted here as a reminder.
    
    image_numberCursor.execute("""INSERT INTO image_taken VALUES({}, "{}")""".format(max_file_number,dtime.datetime.now().time().strftime("%H:%M")) )
    ###################################################################################################################################

    


    
    connection_number_log.commit()

    GPIO.output(RedLedPin_1, False)
    GPIO.output(RedLedPin_2, False)
    GPIO.output(RedLedPin_3, False)
    GPIO.output(RedLedPin_4, False)
    GPIO.output(GreenLedPin,True)
    
    print('Done')
    return 0

def destroy ():
    GPIO.cleanup()
    connection_number_log.close()

def on_press(key): 

    if str(key) == "u'.'":
        take_a_photo()
    elif str(key) == "u'x'":
        Listener.stop()

        destroy()
        
    else:
        print('nichts')
        pass


##Change Folder
os.chdir("/media/pi/Marten/photo_folder")

global connection_number_log
global image_numberCursor
connection_number_log = sq.connect('/home/pi/rasberry/party_photobox/stats_dats/image_taken.dat',check_same_thread=False)
image_numberCursor = connection_number_log.cursor()


## Let's take some pictures!!
setup()
while True:

	try:    
    		with Listener( on_press=on_press,) as listener:
        		listener.join()
	except KeyboardInterrupt:
    		destroy()
    		

