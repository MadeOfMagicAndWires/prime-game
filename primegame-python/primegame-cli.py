#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from utils import *
from primegame import *
import cmd


_LINE="-"*80

##TERMINAL COLORS
_COLOR_RESET = '\033[0m'



class PrimeGameCmd(cmd.Cmd):

    def __init__(self, config_path=""):
        cmd.Cmd.__init__(self)
        self.game = PrimeGame(config_path)
        self._intro()
        self.prompt = "menu>"

    def _print_centered(self, msg):
        print("{:^80}".format(msg))

    def _intro(self):
        self.intro = (_LINE + NEWLINES[sys.platform])
        self.intro += (format("Welcome to Primegame", '^80') +
            NEWLINES[sys.platform])
        self.intro += (_LINE + NEWLINES[sys.platform])

    def _print_highscores(self):
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

    def _print_settings(self, option=""):
        """
        Prints the settings to the screen
        """
        settings = self.game.manager.get_config()

        if not option:
            print("Current settings:")
            for section in settings.sections():
                if not settings.options(section):
                    pass
                else:
                    print("{0:>8}[{s}]".format("", s = section))
                    for option in settings.options(section):
                        value = settings.get(section, option)
                        print("{:>10}{o} = {v}".format("",o = option, v = value))
        else:
            for section in settings.sections():
                if settings.has_option(section, option):
                    print("{0:>}{o} = {v}".format("", o = option, v = settings.get(section, option)))


    def _print_defaults(self, option=""):
        print("DEFAULT settings:")

        if PY3:
            for section, options in DEFAULT_CONFIG.items():
                if not options:
                    pass
                else:
                    print("{0:>8}[{s}]".format("", s = section))
                    for option,value in options.items():
                        print("{0:>10}{o} = {v}".format("", o = option, v = value))

        else:
            for section, options in DEFAULT_CONFIG.iteritems():
                if not options:
                    pass
                else:
                    print("{0:>8}[{s}]".format("", s = section))
                    for option,value in options.iteritems():
                        print("{0:>10}{o} = {v}".format("", o = option, v = value))



    def do_settings(self, args):
        """
        Show and edit the application settings
        """
        if not args:
            self._print_settings()

        else:
            argslist = args.split(" ")
            print(argslist)
            if 'default' in argslist[0][:7]:
                self._print_defaults()
            elif 'set' in argslist[0]:
                print("set")


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
                print("Too bad!")
                if self.game.get_score() <= 0:
                    self.print_centered("Game over!")
                    playing = False

        if self.game.manager.check_highscore(self.game.get_score()):
            print_centered("New highscore!")

            name = get_str("Please insert your name:")

            if not name:
                name = "-"
            self.game.manager.add_highscore(self.game.get_score(), name)


    def do_highscores(self, args):
        """
        no extra arguments: prints the highscores to the screen.
        'clear': clears all highscores (back to default)
        'save' : saves the highscores to the file specified in the configuration
        """
        if not args:
            self._print_highscores()
        elif 'clear' in args:
            print("Are you sure you want to remove ALL highscores?")
            answer = get_str("yes/no:")

            if answer in ('yes', 'y'):
                self.game.manager.highscores = DEFAULT_HIGHSCORES
                self.game.manager.write_highscores(self.game.manager.get_highscore_path())
            else:
                pass
        elif 'save' in args:
            self.game.manager.write_highscores(self.game.manager.get_highscore_path())

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
            open(self.game.manager.get_config_path(),'x')
            self.game.manager.write_config(self.game.manager.get_config_path())
            open(self.game.manager.get_highscore_path(), 'x')
            self.game.manager.write_highscores(self.game.manager.get_highscore_path())
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
        return self.do_quit(args)


if __name__ == "__main__":
    main_cmd = PrimeGameCmd(DEFAULT_CONFIG_PATH)
    main_cmd.cmdloop()
