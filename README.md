# Photobox

A Photobox that will take magnificent images of your party.

__If you have new ideas, need to modify the code or find any bugs, please leave an issue.
So  the Photobox can be developed to a more univeral program in a later version.__

## What do you need?

To set everything up you need
- a Telegram-Account
- a Raspberry Pi
- a camera that is gphoto compatible. You might find the list [here](http://www.gphoto.org/doc/remote/)
- a mouse, keyboard or any other trigger to release your raspi to tell the camera to take pictures.

## How to start

Here everything to set up your Photobox will be explained briefly.

### Installation
Install the required packages:

```bash
sudo apt-get install gphoto2
sudo apt-get install imagemagick
pip install RPi.GPIO
pip install sh
pip instal pynput
pip install telepot
pip install flask
pip install flask_socketio
pip --no-cache-dir install matplotlib   # optimized for low memory on raspi
```

### Generating your Bot

In Telegram search for the BotFather and ask it to create you a new bot.
You might as well read the [Telegram Bot Website](https://core.telegram.org/bots) to help you in doing so.
If you are impatient and want to start right away, jump to part 6. BotFather.

Choose a cool name for your Bot and generate it with the help of BotFather.
If you have generated your Bot the BotFather will send you the ID of your Bot.
It might look like `110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`.

### Configuring your Photobox

With that set up, you can start to configure your Bot.
1. You need to create a file named `ID.txt` in your Photobox repo. Here you need to insert
   the ID of your telegram bot. BotFather send it to you.
2. You need to create a file named `key.txt`. This will be the login code users have to enter
   the first time they have contact to the bot.
3. Configure the `configuration.py` accordingly to your setup.

#### Set the admin ID of your Photobox
You need to change the `admin_id.txt`. There the User-ID of the admin
(host of the photobox, e.g. you) is saved. The ID is required because the admin receives
an error report everytime an error occurs.

Just start a terminal in your repo folder and type
```bash
python telegram.py
```
this will start the telegram bot. Now you need to go to your Telegram account and search for
your bot. Start it and it will send you the admin ID. Terminate the telegram bot for now.

Write the ID send to you into the `admin_id.txt`

Now you are all set. And your Photobox is ready for operation.

### Starting the Photobox

After installing all essential packages and configuring your telegram bot just run the following:

```bash
sh start.sh
```

## Errors

If the PhotoBox is not working you might have to change your code in `photo.py line 31`.
It depends on the output name of the image.