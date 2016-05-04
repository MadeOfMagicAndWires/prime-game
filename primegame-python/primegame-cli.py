# -*- coding: utf-8 -*-

import sys
import os
from utils import *
from primegame import *

class PrimeGameCli(PrimeGame):

    def __init__(self, configpath=""):
        PrimeGame.__init__(self, configpath)

    def play(self):
        """
        Play the game
        """
        raise NotImplementedError

    def show_settings(self):
        """
        Show all current settings
        """

        raise NotImplementedError

    def show_highscores(self):
        """
        Prints the highscores to the screen
        """

        highscores = self.manager.get_highscores()

        ##find the "longest" number.
        nullpadding = len(str(max(highscores.keys())))

        for key in sorted(highscores.keys(), reverse=True):
            value = highscores[key]

            ##print as zeropadded score:name (00500: Scanlan)
            print("{0:0{1}d} : {2}".format(key, nullpadding, value))


    def quit(self):
        """
        Quit the application
        """
        ##Write files if they don't already exist
        try:
            open(self.manager.get_configpath(),'x')
            self.write_config()
            open(self.manager.get_highscorepath(), 'x')
            self.manager.write_highscores()
        except FileExistsError:
            pass
        finally:
            exit()

    def menu(self):
        """
        Show the main menu, alliwing the user to navigate between the various modes
        """

        running = True
        while running:
            if utils.PY3: ##if running python3:
                prompt = str(input("menu>")).lower()
            else:
                prompt = str(raw_input("menu>")).lower()

            if not prompt or prompt not in COMMANDS.values():
                self.quit()
            else:
                if prompt == COMMANDS['highscores'] \
                or prompt == COMMANDS['highscores-alias']:
                    self.show_highscores()
                elif prompt == COMMANDS['play'] \
                or prompt == COMMANDS['play-alias']:
                    self.play()
                elif prompt == COMMANDS['settings'] \
                or prompt == COMMANDS['settings-alias']:
                    self.setting()
                elif prompt == COMMANDS['quit'] \
                or prompt == COMMANDS['quit-alias']:
                    self.quit()
                elif prompt == COMMANDS['help'] \
                or prompt == COMMANDS['help-alias']:
                    self.game_help()
                else:
                    self.game_help()


if __name__ == "__main__":
    game = PrimeGameCli(DEFAULT_CONFIGPATH)
    game.menu()
