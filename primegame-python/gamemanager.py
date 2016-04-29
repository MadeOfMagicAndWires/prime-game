#!/usr/bin/env python

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


class GameManager(object):
    """
    Manages generic game aspects like reading configurations, keeping track of highscores, and a basic menu.
    """

    def __init__(self, configpath="", highscorespath=""):
        
        self.configpath = configpath
        self.highscorespath = highscorespath

    def get_highscorepath(self):
        return self.highscorepath

    def get_configpath(self):
        return self.configpath
    
    def highscores(self):
        return NotImplementedError

    def play(self):
        return NotImplementedError

    def quit(self):
        exit()

    def game_help(self):
        print(u'¯\_(ツ)_/¯')
        return NotImplementedError

    def menu(self):
        running = True
        while running:
            prompt = str(input(">")).lower()
            if not prompt or prompt not in COMMANDS.values():
                quit()
            else:
                if prompt == COMMANDS['highscore'] or prompt == COMMANDS['highscore-alias']:
                    self.highscore()
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
    game = GameManager()
    game.menu()

