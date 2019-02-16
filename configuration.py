homefolder = '/home/pi/repos/Photobox' # folder on your pi where the repo is located
imagefolder = "/home/pi/Pictures"      # folder where to save images taken

photo_key = "u'.'"  # key to press in order to record an image
stop_key = "u'x'"   # key to terminate the photo.py

admin = 'Henning'   # name of the admin

keyfile = 'key.txt' # file with the login key

# configures the flask web app
image_width = '1232'   # define image dimensions. If you take smaller dimensions
image_height = '816'   # than the original, remember to keep the aspect ratio
bg_color = '#000000'   # color of the image background 
font_color = '#999999' # color of the displayed image number