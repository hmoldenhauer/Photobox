#!/bin/bash
WANTED=gvfsd-gphoto2

# check if WANTED exists and kill it
if pidof $WANTED > /dev/null ; then
    echo "$WANTED is going to be killed"
    $(kill $(pidof $WANTED))
else
    echo "$WANTED has already been killed"
fi

# start the scripts for the Photobox
echo "starting the Photobox"
$(python photo.py & python telegram.py & FLASK_APP=webinterface.py flask run &)