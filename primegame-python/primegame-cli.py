#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple command line interface to play the primegame with

Usage:
    primegame-cli [-conf|--conf 'filename']

    flags:
        -conf --conf 'filename' =
            start primegame with the
            alternative configuration file 'filename'


PrimeGameCmd = cmd.Cmd class that handles the interface
cmd_help = prints general help message for the cli
LINE = a seperation line of 80 '-' characters
COLOR_RESET = terminal character to reset the text colour

"""

import sys
import os
from utils import *
from primegame import *
import cmd


LINE="-"*80

# TERMINAL COLORS
COLOR_RESET = '\033[0m'



class PrimeGameCmd(cmd.Cmd):
    """
    Provides a basic command line user interface
    to play the primegame game

    """

    def __init__(self, config_path=""):
        """
        Initialiser for the class

        arguments:
            config_path = path to configuration file to use for
                          the game

        """
        cmd.Cmd.__init__(self)
        self.game = PrimeGame(config_path)
        self._intro()
        self.prompt = "menu>"

    def _print_centered(self, msg):
        """
        Prints a message to the terminal that is center-aligned

        Assumes the window has a width of 80 characters

        arguments:
            msg = the message to be printed

        """
        print("{:^80}".format(msg))


    def _print_indented(self,msg="", tabs_amount=1):
        """
        Prints a message to the terminal tab indented

        arguments:
            msg = the message to be printed
            tabs_amount = amount of tabs preceding

        """

        tabs_str = "\t" * tabs_amount
        print(tabs_str + msg)

    def _intro(self):
        """
        Sets the intro message for the CLI

        """

        #self.intro will be displayed on start-up
        self.intro = (LINE + NEWLINES[sys.platform])
        self.intro += (format("Welcome to Primegame", '^80') +
            NEWLINES[sys.platform])
        self.intro += (LINE + NEWLINES[sys.platform])

    def _print_highscores(self):
        """
        Prints the highscores to the screen

        """
        highscores = self.game.manager.get_highscores()

        # find the "longest" number, needed for zeropadding
        nullpadding = len(str(max(highscores.keys())))

        # print highscores as zeropadded score:name (00500: Scanlan etc.)
        for key in sorted(highscores.keys(), reverse=True):
            value = highscores[key]

            print("{0:0{1}d} : {2}".format(key, nullpadding, value))

    def _print_settings(self, option=[]):
        """
        Prints the settings and their values to the screen

        arguments:
            (optional) options_list = when given it will *only* print
                                      the settings and values defined
                                      in the list

        """
        settings = self.game.manager.get_config()


        if not option: # just print all settings version
            print("Current settings:")
            print()

            # for each configuration section print the section name
            # and it's containing settings and corrosponding values
            for section in settings.sections():
                if not settings.options(section):
                    pass
                else:
                    # print "[Configuration section]"
                    self._print_indented("[{}]".format(section))
                    for option in settings.options(section):
                        value = settings.get(section, option)
                        # print in the format "setting = value"
                        self._print_indented("{o} = {v}".format(o = option, v = value), 2)


        else: # 'settings get' version
            for arg in option:
                # keep track if setting is set
                has_setting = False

                for section in settings.sections():
                    if settings.has_option(section, arg):

                        # print "[Configuration section]"
                        self._print_indented("[{}]".format(section))

                        # double indent, now it's even worse
                        # format is "setting = value"
                        self._print_indented(
                                "{o} = {v}".format(o = arg,
                                    v = settings.get(section, arg)), 2)

                        # setting is set, we're done
                        has_setting = True
                    else:
                        pass

                if not has_setting:
                    # setting does not exist in current configuration
                    # so we print "setting = Undefined"
                    self._print_indented("{1} = Undefined".format("", arg), 2)


    def _print_default_settings(self, options_list=[]):
        """
        Prints the default settings and their values to the screen

        arguments:
            (optional) options_list = when given it will *only* print
                                      the settings and values defined
                                      in the list

        """

        # No extra arguments given, print all settings
        if not options_list:
            print("DEFAULT settings:")
            print()

            # for each configuration section print the section name
            # and it's containing settings and corrosponding values
            if PY3:
                for section, options in DEFAULT_CONFIG.items():
                    if not options:
                        pass
                    else:
                        self._print_indented("[{}]".format(section))
                        for option,value in options.items():
                            self._print_indented("{o} = {v}".format(o = option, v = value), 2)

            # Do the same when running python 2
            else:
                for section, options in DEFAULT_CONFIG.iteritems():
                    if not options:
                        pass
                    else:
                        self._print_indented("[{}]".format(section))
                        print(print_tab("[{}]".format(section)))
                        for option,value in options.iteritems():
                            self._print_indented("{o} = {v}".format(o = option, v = value), 2)

        # extra arguments given, print only selected settings and their values
        else:
            # for each setting given, check if it's in the default configuration
            for arg in options_list:
                has_setting = False
                if PY3:
                    for section,options in DEFAULT_CONFIG.items():
                        if arg in options:
                            value = options[arg]
                            self._print_indented("[{}]".format(section))
                            self._print_indented("{o} = {v}".format(o = arg, v = value), 2)
                            has_setting = True
                        else:
                            pass

                # do the same when running python 2
                else:
                    for section,options in DEFAULT_CONFIG.iteritems():
                        if arg in options:
                            value = options[arg]
                            self._print_indented("[{}]".format(section))
                            self._print_indented("{o} = {v}".format(o = arg, v = value), 2)
                            has_setting = True
                        else:
                            pass

                # given setting does not exist in the default configuration,
                # set value to undefined
                if not has_setting:
                    print(print_tab("{0:>2}{1} = Undefined".format("", arg)))


    def _set_setting(self, option="", value=""):
        """
        Change a setting and save the new configuration

        arguments:
            option = the name of the setting to change or create
            value  = the value that this setting will be set to

        """

        settings = self.game.manager.get_config()
        written_setting = False

        # First check if the setting is already present
        # in any configuration section.
        # if it is, change that section
        # Otherwise, create a new setting in the section 'general'
        if PY3:
            for section,options in DEFAULT_CONFIG.items():
                if option in options:
                    self.game.manager.set_setting(option, value, section)
                    written_setting = True
                else:
                    pass
            if not written_setting:
                self.game.manager.set_setting(option, value)

        # do the same in python 2
        else:
            for section,options in DEFAULT_CONFIG.iteritems():
                if option in options:
                    self.game.manager.set_setting(option, value, section)
                    written_setting = True
                else:
                    pass
            if not written_setting:
                self.game.manager.set_setting(option, value)

        self._print_settings([option])

    def do_settings(self, args):
        """
        Show or edit the application configuration

        Usage:
            no extra arguments: prints the configuration

            defaults: prints the default configuration values

            get 'option': only prints the single option 'option'
                          and it's value

            set 'option' 'value': configures the option 'option'
                                  with value 'value'

        arguments:
            args = the extra arguments given in the cli
                   (see usage for possible arguments)

        """

        # No extra arguments given
        if not args:
            self._print_settings()

        # check the extra arguments and handle them accordingly
        else:
            argslist = args.split(" ")

            # print defaults
            if 'default' in argslist[0][:7]:
                if argslist[1:]:
                    self._print_default_settings(argslist[1:])
                else:
                    self._print_default_settings()

            # get selected settings
            elif 'get' in argslist[0]:
                self._print_settings(argslist[1:])

            # set seletced setting
            elif 'set' in argslist[0][:3]:
                if len(argslist) == 3:
                    self._set_setting(argslist[1], argslist[2])
                else:
                    print("wrong number of arguments.")
                    print("Type 'help settings' for information")

            # reset to defaults
            elif 'reset' in argslist[0]:
                self._print_centered("This will reset the entire configuration")
                self._print_centered("to the default settings and values")
                self._print_centered("Are you sure?")

                answer = get_str("yes/no:")

                if answer in ('yes', 'y', 'ye'):
                    for section in self.game.manager.config.sections():
                        self.game.manager.config.remove_section(section)

                    self.game.manager.config = self.game.manager.default_settings(self.game.manager.config)
                    self.game.manager.write_config(self.game.manager.get_config_path())
                else:
                    pass

            # manually save the current configuration
            elif 'save' in argslist[0]:
                self.game.manager.write_config(self.game.manager.get_config_path())

            # extra argument is not recognized
            else:
                pass

    def do_play(self, args):
        """
        Starts the game

        Whilst playing the user has to guess
        whether the current number is a prime or not
        until the player loses (score is reduced to zero) or ends on a high.

        Usage:
            yes/y: true (the current number is a prime)
            no/n:  false (the current number **isn't** a prime)
            quit/q/stop: quit the game

        """

        self.game.reset_score()
        playing = True

        # start running the game
        while playing:
            clear()
            print("{:^80}".format(self.game.__str__()))
            print(LINE)
            print("{:^80}".format(self.game.get_number()))
            print("{:^80}".format("Is this a prime?"))
            print(LINE)
            print()

            correct = True

            # prompt the user for input , and handle their response
            answer = get_str("yes/no:")
            if not answer:
                playing = False
            else:
                # user thinks the current number is a prime
                if answer in ('yes', 'y'):
                    correct = self.game.play_turn(True)

                # user thinks the current number *isn't* a prime
                elif answer in ('no', 'n'):
                    correct = self.game.play_turn(False)

                # user would like to quit playing this stupid game
                elif answer in ('quit', 'q', 'stop'):
                    playing = False


            if not correct:
                print("Too bad!")
                # If the score hits the limit of 0, end the game
                if self.game.get_score() <= 0:
                    self.print_centered("Game over!")
                    playing = False

        # Once the game is over, check for highscore
        # if a new highscore has been reached
        # prompt the user for their name and save the new score
        if self.game.manager.check_highscore(self.game.get_score()):
            self._print_centered("New highscore!")

            name = get_str("Please insert your name:")
            self.game.manager.add_highscore(self.game.get_score(), name)


    def do_highscores(self, args):
        """
        Prints, saves, and/or clears the highscores

        Usage:
            no extra arguments: prints the highscores to the screen.
            'clear': clears all highscores (back to default)
            'save' : saves the highscores to the file specified in the configuration

        arguments:
            args = the extra arguments given in the cli
                   (see usage for possible args)

        """

        # no extra arguments given, print the current highscores
        if not args:
            self._print_highscores()

        # otherwise handle the extra arguments
        elif 'clear' in args: # etra argument was 'clear'
            print("Are you sure you want to remove ALL highscores?")
            answer = get_bool("yes/no:")

            # check confirmation,
            # if true, reset the highscores to the highscores
            # defined in gamemanager.DEFAULT_HIGHSCORES
            if answer:
                self.game.manager.highscores = DEFAULT_HIGHSCORES
                self.game.manager.write_highscores(self.game.manager.get_highscore_path())
            else:
                pass
        # extra argument was 'save', manually write highscores to file
        elif 'save' in args:
            self.game.manager.write_highscores(self.game.manager.get_highscore_path())

    # alias function
    def do_high(self, args):
        """
        Alias for 'highscores'

        See 'help highscores' or do_highscores for more info

        """
        self.do_highscores(args)

    def do_quit(self, args=0):
        """
        Quit the application and save any changed user data

        """
        self.game.manager.save_data(self.game.manager.get_config_path(), self.game.manager.get_highscore_path())
        return True

    # alias function
    def do_q(self, args):
        """
        Alias for 'quit'

        See 'help quit' or do_quit for more info

        """
        return self.do_quit(args)

    # alias function
    def do_EOF(self, args):
        """
        Alias for 'quit'

        See 'help quit' or do_quit for more info

        """
        return self.do_quit(args)


if __name__ == "__main__":

    def cmd_help(errmsg=""):
        """
        Prints general usage help, preceded by a possible error message.

        """
        # if an error message was included, print that as well
        if errmsg:
            eprint(errmsg)

        print("Usage:")
        print("no arguments: {0:>11}{1}".format("", "start primegame"))
        print("--conf -conf 'filename': start primegame with")
        print("{0:>25}{1}".format("", "alternative configuration file 'filename'"))

    # initiate main_cmd to begin, might still change
    main_cmd = PrimeGameCmd(DEFAULT_CONFIG_PATH)

    #Check for command line arguments
    if len(sys.argv) > 1:

        argv_iter = iter(sys.argv[1:])

        # iterate command line arguments
        for arg in argv_iter:
            if arg[:1] == "-": # only allow - and --flags
                if arg in ('-conf', '--conf'):
                    #  -conf or --conf flag to set alternative config file
                    #  change main_cmd to use alternative config file
                    main_cmd = PrimeGameCmd(next(argv_iter))
                else:
                    # flag does not exist, print error
                    eprint("Unknown Argument '{}'".format(arg))

            else:
                # Not a - or --flag, print error and help
                cmd_help("Illegal Argument '{}'".format(arg))
                exit(1)

    main_cmd.cmdloop()
