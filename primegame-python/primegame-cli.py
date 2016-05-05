# -*- coding: utf-8 -*-

import sys
import os
from utils import *
from primegame import *
import cmd

LINE="-"*80


class PrimeGameCmd(cmd.Cmd):

    def __init__(self, configpath=""):
        cmd.Cmd.__init__(self)
        self.game = PrimeGame(configpath)
        self._intro()

    def _intro(self):
        self.intro = (LINE + NEWLINES[sys.platform])
        self.intro += (format("Welcome to Primegame", '^80') +
            NEWLINES[sys.platform])
        self.intro += (LINE + NEWLINES[sys.platform])

    def do_play(self, args):
        """
        Play the game
        """

        self.game.reset_score()
        playing = True

        while playing:
            clear()
            print("{:^80}".format(self.game.__str__()))
            print(LINE)
            print("{:^80}".format(self.game.get_number()))
            print("{:^80}".format("Is this a prime?"))
            print(LINE)
            print()

            correct = True

            answer = get_str("yes/no:")
            if not answer:
                playing = False
            else:
                if answer in ('yes', 'y'):
                    correct = self.game.play_turn(True)

                elif answer in ('no', 'n'):
                    correct = self.game.play_turn(False)

                elif answer in ('quit', 'q', 'stop'):
                    playing = False

            if not correct:
                if self.game.get_score() <= 0:
                    print("{:^80}".format("Game over!"))
                    playing = False

        if self.game.manager.check_highscore(self.game.get_score()):
            print("{:^80}".format("New highscore!"))

            name = get_str("Please insert your name:")

            if not name:
                name = "-"
            self.game.manager.add_highscore(self.game.get_score(), name)

    def do_settings(self, args):
        """
        Show and edit the application settings
        """
        raise NotImplementedError

    def do_highscores(self, args):
        """
        Prints the highscores to the screen
        """

        highscores = self.game.manager.get_highscores()

        ##find the "longest" number.
        nullpadding = len(str(max(highscores.keys())))

        for key in sorted(highscores.keys(), reverse=True):
            value = highscores[key]

            ##print as zeropadded score:name (00500: Scanlan)
            print("{0:0{1}d} : {2}".format(key, nullpadding, value))

    def do_high(self, args):
        """
        Prints the highscores to the screen
        """
        self.do_highscores(args)

    def do_quit(self, args=0):
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
            return True

    def do_q(self, args):
        """
        Quit the application
        """
        return self.do_quit(args)

    def do_EOF(self, args):
        """
        Quit the application
        """
        return self.do_quit(self, args)


if __name__ == "__main__":
    main_cmd = PrimeGameCmd(DEFAULT_CONFIGPATH)
    main_cmd.cmdloop()
