#!/bin/bash
WANTED=gvfsd-gphoto2

if pidof $WANTED > /dev/null ; then
    echo "$WANTED is going to be killed"
    $(kill $(pidof $WANTED))
else
    echo "$WANTED has already been killed"
fi

echo "starting the Photobox"
$(python photo.py & python telegram.py & FLASK_APP=webinterface.py flask run &)