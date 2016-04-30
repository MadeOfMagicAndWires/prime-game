#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import csv
import utils




COMMANDS={
        'highscore': 'highscore',
        'highscore-alias': 'high',
        'play': 'play',
        'play-alias': 'p',
        'quit': 'quit',
        'quit-alias': 'q',
        'help': 'help',
        'help-alias': 'h'
        }


DEFAULT_HIGHSCOREPATH="highscores.csv"
DEFAULT_CONFIG="config.ini"

DEFAULT_HIGHSCORES={
        'Vax' : 6000,
        'Vex' : 3000,
        'Pyke': 2000,
        'Grog': 10000,
        'Percy': 200,
        'Keyleth': 400,
        'Tiberius': 0,
        'Scanlan': 500,
        }

class GameManager(object):
    """
    Manages generic game aspects like reading configurations, keeping track of highscores, and a basic menu.
    """

    def __init__(self, configpath="", highscorespath=""):

        self.configpath = configpath
        self.highscorespath = highscorespath
        self.highscores = self.load_highscores()

    def get_configpath(self):
        return self.configpath

    def get_highscorepath(self):
        return self.highscorepath

    def get_highscores(self):
        return self.highscores

    def load_highscores(self):
        highscores = dict()

        try:
            with open(self.highscorespath, 'rU', newline=utils.NEWLINES[sys.platform]) as ftest:
                pass
        except IOError as e:
            print(e.message)
            highscores = DEFAULT_HIGHSCORES

        with open(self.highscorespath, 'rU', newline=utils.NEWLINES[sys.platform]) as f:
            csvalues = csv.reader(f)

            try:
                csvalues.next()
            except AttributeError:
                csvalues.__next__()

            highscores = dict()
            for row in csvalues:
                highscores[row[0]]= int(row[1])


        if not highscores:
            highscores = DEFAULT_HIGHSCORES

        return highscores


    def print_highscores(self):

        highscores = list()
        sortkey=lambda x:x[1]


        try:
            for key,value in sorted(self.highscores.items(), key=sortkey, reverse=True):
                print("{} : {}".format(key, value, align='right aligned'))
        except AttributeError:
            for key,value in sorted(self.highscores.iteritems(), key=sortkey, reverse=True):
                print("{} : {}".format(key, value, align='right aligned'))

    def write_highscores(self):
        print("Saving highscores...".format('right aligned'))

        try:
            with open(self.highscorespath, 'w', newline=utils.NEWLINES[sys.platform]) as highscoresf:
                fieldnames = ('name', 'score')
                writer = csv.DictWriter(highscoresf, fieldnames)

                writer.writeheader()

                sortkey= lambda x:x[1]

                try:
                    for key,value in sorted(self.highscores.items(), key=sortkey, reverse=True):
                        writer.writerow({fieldnames[0]:key, fieldnames[1]: value})
                except AttributeError:
                    for key,value in sorted(self.highscores.iteritems(), key=sortkey, reverse=True):
                        writer.writerow({fieldnames[0]:key, fieldnames[1]: value})
                finally:
                    print("Success!")

        except IOError as e:
            print(e.message)


    def add_highscore(self, new_highscore):
        return NotImplementedError

    def play(self):
        return NotImplementedError

    def quit(self):
        self.write_highscores()
        exit()


    def game_help(self):
        print(u'¯\_(ツ)_/¯')
        return NotImplementedError

    def menu(self):
        running = True
        while running:
            try:
                prompt = str(input(">")).lower()
            except NameError:
                prompt = str(raw_input(">")).lower()

            if not prompt or prompt not in COMMANDS.values():
                quit()
            else:
                if prompt == COMMANDS['highscore'] or prompt == COMMANDS['highscore-alias']:
                    self.print_highscores()
                elif prompt == COMMANDS.get('play') or prompt == COMMANDS.get('play-alias'):
                    self.play()
                elif prompt == COMMANDS['quit'] or prompt == COMMANDS['quit-alias']:
                    self.quit()
                elif prompt == COMMANDS['help'] or prompt == COMMANDS['help-alias']:
                    self.game_help()
                else:
                    self.game_help()

if __name__ == "__main__":
    import sys
    game = GameManager(DEFAULT_CONFIG,DEFAULT_HIGHSCOREPATH)
    game.menu()

