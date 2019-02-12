# -*- coding: utf-8 -*-
import telepot as tp
from telepot.loop import MessageLoop
import numpy as np
import os
import time
import datetime as dtime
import sqlite3 as sq
from collections import Counter
import matplotlib.pyplot as plt

from configuration import *

# get the ID of your telegram bot
def get_ID(ID_file):
    try:
        with open(ID_file, 'r') as f:
            # [:-1] to cut '\n'
            ID = f.readline()[:-1]

            if ID == '\n':
                print('No ID included in ' + ID_file)
            else:
                return ID
    except IOError:
        print('No file found with the name ' + ID_file)


class PiPhotobox(object):

    def __init__(self,path_to_admin_id):
        # id of the photobox admin
        self.admin_id = int(np.genfromtxt(path_to_admin_id,unpack = True))
        # key needed to be allowed to get images
        self.key = get_ID(keyfile)

        # user_auth is a db to save the authorization data
        self.connection_user_auth = sq.connect(homefolder + '/stats_dats/user_auth.dat', check_same_thread=False)
        # user_log is a db to save the user_data
        self.connection_user_log = sq.connect(homefolder + '/stats_dats/user_log.dat', check_same_thread=False)
        # image_taken is a db to keep track of all taken images
        self.connection_number_log = sq.connect(homefolder + '/stats_dats/image_taken.dat', check_same_thread=False)
        # get the cursor to both db's
        self.authCursor = self.connection_user_auth.cursor()
        self.baseCursor = self.connection_user_log.cursor()
        self.image_numberCursor = self.connection_number_log.cursor()

    def end_connection(self):
        self.connection_user_auth.close()
        self.connection_user_log.close()
        self.connection_number_log.close()


    ##########################################################################################################################
    ### Function to generated a Bar plot, thats shows which user requested how many images ###################################
    ##########################################################################################################################
    def name_downloads_statistic(self,chat_id):
      self.baseCursor = self.connection_user_log.cursor()
      self.baseCursor.execute(""" SELECT Username FROM user_log""")

      ### Generate the data
      name_list = []
      number_list = []
      for element in Counter(self.baseCursor.fetchall()).most_common():
        name_list.append(element[0][0])
        number_list.append(element[1])

      ### Generate Plot
      plt.clf()
      x_pos = np.arange(len(name_list))
      plt.bar(x_pos,number_list)
      plt.xticks(x_pos,name_list)
      plt.ylabel('Anzahl Downloads')
      plt.savefig(homefolder + '/stats_dats/user_statistic.png')

      ### Send requested Plot to the User
      piBot.sendMessage(chat_id, str('Hier die Nutzerstatistik:'))
      piBot.sendPhoto(chat_id, photo=open(homefolder + '/stats_dats/user_statistic.png', 'rb'))

      return 0

    ###########################################################################################################################################################################
    ### Function to generated a Histogram, which shows the how often a image was got a download request. Further, you get the image number of the two most requested images ###
    ###########################################################################################################################################################################
    def most_popular_statistic(self,chat_id):

      self.baseCursor.execute(""" SELECT Image_Number FROM user_log""")

      ### Generated a List with all Imagenumber
      image_number_log = [ i[0] for i in self.baseCursor.fetchall()]

      ### Plot a histogramm
      plt.clf()
      plt.hist(image_number_log, bins=range(min(image_number_log), max(image_number_log) + 2, 1), rwidth=0.95 )
      plt.grid(axis='y', alpha = 0.8)
      plt.xticks(range(min(image_number_log), max(image_number_log) + 2, 1))
      plt.xlabel('Bildnummer')
      plt.ylabel('Anzahl Downloads')
      plt.savefig(homefolder + '/stats_dats/number_downloads.jpg')

      #### Generate a list with the two most requested images ##############################################################################
      image_number_log_max = Counter(image_number_log).most_common(2) ## Get the number with the most requests

      ## Send the requested stats
      piBot.sendMessage(chat_id, 'Bildnummer ' + str(image_number_log_max[0][0]) +'\n ist im Moment mit ' + str(image_number_log_max[0][1]) + ' Downloads, dass gefragteste Bild. \n\n'
        'Dahinter ist Bildnummer ' + str(image_number_log_max[1][0]) + ' \n mit ' + str(image_number_log_max[1][1]) + ' Downloads, dass zweit gefragteste Bild.')

      piBot.sendMessage(chat_id, str('Hier ist die Fotonnachfragestatistik:'))
      piBot.sendPhoto(chat_id, photo=open(homefolder + '/stats_dats/number_downloads.jpg', 'rb'))

      return 0

    ##########################################################################################################################
    ### Function to generated a timebased Histogram, that shows how many images were downloaded during a spezific timeslot ###
    ##########################################################################################################################
    def time_based_statistic(self,chat_id,name):

      if name == 'timebased':
          self.baseCursor.execute(""" SELECT Time_Stampt FROM user_log""")
          ylabel_name = 'Anzahl Downloads'
          ### Generate a int list with all the timestamps. A Stamp is formatted like this: '20:30'
          time_stampt_list = [ int(i[0].split(':')[0]) for i in self.baseCursor.fetchall()]

      elif name == 'taken':
          self.image_numberCursor.execute(""" SELECT Time_Stampt FROM image_taken""")
          ylabel_name = 'Anzahl Fotos'
          time_stampt_list = [ int(i[0].split(':')[0]) for i in self.image_numberCursor.fetchall()]

      else:
        pass

      ### Generated a plot
      plt.clf()
      plt.hist(time_stampt_list,  bins=range(min(time_stampt_list), max(time_stampt_list) + 2, 1), rwidth=0.95 )
      plt.xticks(range(min(time_stampt_list), max(time_stampt_list) + 2, 1))
      plt.xlabel('Uhrzeit')
      plt.ylabel(ylabel_name)
      plt.grid(axis='y', alpha = 0.8)
      plt.savefig(homefolder + '/stats_dats/time_based_statistic.jpg')

      piBot.sendMessage(chat_id, str('Hier ist die zeitaufgelöste Statistik:'))
      piBot.sendPhoto(chat_id, photo=open(homefolder + '/stats_dats/time_based_statistic.jpg', 'rb'))

      return 0

    def send_image(self, msg):
        # Get the required information of a request
        # message text
        command = msg['text']
        # chat_id = Who has sent the message
        chat_id = msg['chat']['id']
        # What was the username of the person who has requested an image or plot
        chat_name =  msg['chat']['username']

        # check if bot is configured properly
        if self.admin_id == 1:
            chat_id = msg['chat']['id']
            piBot.sendMessage(chat_id, 'Die admin-id ist: ' + str(chat_id))
        else:
            try:
                self.authCursor.execute("""SELECT Authentification FROM user_auth WHERE Username='{us}'""".format(us=chat_name))
                authorized = self.authCursor.fetchone()[0]

                if authorized == []:
                    if (command == self.key):
                        auth = 1
                        try:
                            self.authCursor.execute("""UPDATE user_auth SET Authentification={au} WHERE Username='{us}'""".format(au=auth, us=chat_name))
                            self.connection_user_auth.commit()
                        except sq.OperationalError:
                            try:
                                self.authCursor.execute("""INSERT INTO user_auth VALUES("{}", {}, "{}")""".format(str(chat_name), auth, str(dtime.datetime.now().time().strftime("%H:%M:%S"))))
                                self.connection_user_auth.commit()
                            except sq.OperationalError:
                                self.authCursor.execute("""CREATE TABLE user_auth (Username TEXT ,Authentification SMALLINT, Time_Stamp TEXT)""")

                                self.authCursor.execute("""INSERT INTO user_auth VALUES("{}", {}, "{}")""".format(str(chat_name), auth, str(dtime.datetime.now().time().strftime("%H:%M:%S"))))
                                self.connection_user_auth.commit()
                                pass
                            pass

                        piBot.sendMessage(chat_id,str('Du kannst die Photobox jetzt nutzen.'))
                    else:
                        piBot.sendMessage(chat_id,str('Du musst zuerst den Code eingeben um die Photobox zu nutzen. Frag ' + admin + ' danach.'))

                elif authorized == 1:
                    # alle funktionen nutzbar
                    ### Split Command message to get the command and eventually the image_number ###

                    command = command.split()
                    # Check the kind of command
                    if (command[0] == u'Image'):

                        # Fehler möglich, bei erstem Bild und erstem User
                        if (command[1] == 'last'):
                            # get number from max_file_number.txt
                            f = open(homefolder + '/stats_dats/max_file_number.txt', 'r')
                            max_file_number = [int(x) for x in next(f).split()]
                            f.close()

                            piBot.sendMessage(chat_id,str('Du erhälst Bild ') + str(max_file_number[0]) )

                            piBot.sendPhoto(chat_id, photo=open('./photobox_small_' + str(max_file_number[0]).zfill(4) + '.jpg', 'rb'))

                            self.baseCursor.execute("""INSERT INTO user_log VALUES("{}", {}, {}, "{}")""".format(str(chat_name),chat_id, int(max_file_number[0]), str(dtime.datetime.now().time().strftime("%H:%M"))) )
                            self.connection_user_log.commit()

                        else:
                            try:
                                piBot.sendMessage(chat_id,str('Du erhälst Bild ') + str(command[1]) )

                                # send image
                                piBot.sendPhoto(chat_id, photo=open('./photobox_small_' + str(command[1]).zfill(4) + '.jpg', 'rb'))

                                self.baseCursor.execute("""INSERT INTO user_log VALUES("{}", {}, {}, "{}")""".format(str(chat_name),chat_id, int(command[1]), str(dtime.datetime.now().time().strftime("%H:%M"))) )
                                self.connection_user_log.commit()

                            # No table was founded error
                            # Solution: Create new table
                            except sq.OperationalError:

                                self.baseCursor.execute(""" CREATE TABLE user_log(Username TEXT ,User_ID SMALLINT, Image_Number SMALLINT,Time_Stampt TEXT)""")
                                self.baseCursor.execute("""INSERT INTO user_log VALUES("{}", {}, {}, "{}")""".format(str(chat_name),chat_id, int(command[1]), str(dtime.datetime.now().time().strftime("%H:%M"))) )
                                self.connection_user_log.commit()
                                pass

                            # The requested image_number does not exist
                            # Solution, Photobox answers the person and sends a message
                            # to the admin
                            except IOError as e:
                                piBot.sendMessage(chat_id, 'Es gibt kein Foto mit der Nummer: ' + str(command[1]) )
                                piBot.sendMessage(self.admin_id, 'Nicht vorhandenes Foto wurde angefragt: ' + str(command[1])+'.\n\n Hier zur Sicherheit nochmal der Fehlercode: \n\n' + str(e) + '\n\n Der ausführende User ist: \n' + str(chat_name))
                                pass

                            # A unknown error occured
                            # Solution, Admin and person gets a message
                            except Exception as e:
                                print(e)
                                piBot.sendMessage(chat_id, 'Ein unbekannter Fehler ist aufgetreten. ' + admin + ' wird benachrichtigt.')
                                piBot.sendMessage(self.admin_id, 'Es ist ein Fehler bei dem verschicken des Fotos mit der Nummer ' + str(command[1]) + ' aufgetreten. Der Fehler Code lautet: \n' + str(e)+ '.\n Auf den Fehler wird mit \pass reagiert. Der verursachende User ist: \n' + str(chat_name))
                                pass

                    elif command[0] == u'Stat':
                        try:
                            # Different possibility of stats
                            if command[1] == u'name':
                                self.name_downloads_statistic(chat_id)

                            elif command[1] == u'popular':
                                self.most_popular_statistic(chat_id)

                            elif command[1] == u'timebased':
                                self.time_based_statistic(chat_id,'timebased')

                            elif command[1] == u'taken':
                                self.time_based_statistic(chat_id,'taken')

                            else:
                                piBot.sendMessage(chat_id, 'Leider ist deine Auswahl nicht dabei.\n Zur Verfügung stehen die Befehle: \n\n --- name --- : Dieser Befehl (ohne die --- ) zeigt dir an welcher User wie viel Bilder gedownloadet hat \n\n --- popular --- \n Dieser Befehl (ohne die --- ) zeigt dir die beliebtesten Bilder \n\n --- timebased--- \n Dieser Befehl (ohne die --- ) zeigt dir wie viele Bilder zu einer bestimmten Uhrzeit (stündlich) gedownloadet wurden \n\n --- taken ---\n Dieser Befehl (ohne die ---) zeigt dir wie viele Bilder zu einer bestimmten Uhrzeit (stündlich) mit der Photobox aufgenommen wurden')
                        except IndexError:
                            piBot.sendMessage(chat_id, 'Du hast das Keyword vergessen.\n Zur Verfügung stehen die Keywords: \n\n --- name --- \n Dieser Befehl (ohne die --- ) zeigt dir an welcher User wie viel Bilder gedownloadet hat \n\n --- popular --- \n Dieser Befehl (ohne die --- ) zeigt dir die beliebtesten Bilder \n\n --- timebased--- \n Dieser Befehl (ohne die --- ) zeigt dir wie viele Bilder zu einer bestimmten Uhrzeit (stündlich) gedownloadet wurden \n\n --- taken ---\n Dieser Befehl (ohne die ---) zeigt dir wie viele Bilder zu einer bestimmten Uhrzeit (stündlich) mit der Photobox aufgenommen wurden')

                    elif command[0] == u'Help':
                        piBot.sendMessage(chat_id, admin + ' wird benachrichtigt.')
                        piBot.sendMessage(self.admin_id,'Hilfeanfrage von: ' + str(chat_name))

                    else:
                        piBot.sendMessage(chat_id, 'Leider ist dein Befehl nicht in der Datenbank verzeichnet.\n Hier nochmal deine Möglichkeiten:\n\n --- Image image_number --- \n Hier erhälst du das Bild mit der Nummer image_number direkt auf dein Handy geschickt.\n Bsp: Image 7\n Um Bildnummer 7 zuerhalten. \n Statt einer Zahl kannst du mit Image last auch das letzte Bild anfordern. \n\n --- Stat keyword ---\n Hier erhälst du verschiedene Nutzerstatistiken der Photobox. Als Keyword stehen zur Verfügung:\n name, popular, timebased und taken.\nBsp:\n stat name \n\n --- Help ---\n Hier wird ' + admin + ' auf seinem Handy benachrichtigt und kommt schnellstmöglichst zu dir. Wenn er nicht kommt solltest du ihn suchen gehen.')


            except sq.OperationalError:
                auth = 0
                try:
                    self.authCursor.execute("""UPDATE user_auth SET Authentification={au} WHERE Username='{us}'""".format(au=auth, us=chat_name))
                    self.connection_user_auth.commit()
                except sq.OperationalError:
                    try:
                        self.authCursor.execute("""INSERT INTO user_auth VALUES("{}", {}, "{}")""".format(str(chat_name), auth, str(dtime.datetime.now().time().strftime("%H:%M:%S"))))
                        self.connection_user_auth.commit()
                    except sq.OperationalError:
                        self.authCursor.execute("""CREATE TABLE user_auth (Username TEXT, Authentification SMALLINT, Time_Stamp TEXT)""")

                        self.authCursor.execute("""INSERT INTO user_auth VALUES("{}", {}, "{}")""".format(str(chat_name), auth, str(dtime.datetime.now().time().strftime("%H:%M:%S"))))
                        self.connection_user_auth.commit()
                        pass
                    pass

                piBot.sendMessage(chat_id,str('Du musst zuerst den Code eingeben um die Photobox zu nutzen. Frag ' + admin + ' danach.'))


### Start Photobox if used as main class
if __name__ == '__main__':
  piBot = tp.Bot( get_ID('ID.txt') )
  piphotobox = PiPhotobox('admin_id.txt')

  os.chdir(imagefolder)

  try:
      # Start the Telegramm chat
      MessageLoop(piBot, piphotobox.send_image).run_as_thread() # Start the Telegramm chat
      print('start')
      while True:
          # Update the chat every second
          time.sleep(1)

  except KeyboardInterrupt:
        print('Programm wird beendet')
        piphotobox.end_connection()
