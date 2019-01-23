# Photobox

## First of all
Some parts of the code has to be modified for different brands.

__Please leave an issue, if you have to modify the code. So that I can release an
universial program code in a later version.__

At this points you have to change your code probably:

1. `photo.py line 51`
It depends on the output name of the image.

2. `photo.py line 83`
This line depends on the output of your presenter


## How to start
First install the required packages:

`sudo apt-get install gphoto2`

`pip install RPi.GPIO`

`pip install sh`

`pip instal pynput`

`pip install telepot`

`pip install flask`

You need a file named `ID.txt` where the ID of your telegram bot is saved.
Also a file is required named `admin_id.txt`, where the User-ID of the admin
(host of the photobox is saved). The ID is required because the admin receives
an error report everytime a error occurs.

After installing all essential packages just run the following three programs:

`python telegram.py`

`python webinterface.py`

`python photo.py`
