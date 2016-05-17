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

    def _print_settings(self, option=[]):
        """
        Prints the settings to the screen
        """
        settings = self.game.manager.get_config()
        print_tab = lambda x: "{0:>8}{1}".format("", x)


        if not option:
            print("Current settings:")
            print()
            for section in settings.sections():
                if not settings.options(section):
                    pass
                else:
                    print(print_tab("[{}]".format(section)))
                    for option in settings.options(section):
                        value = settings.get(section, option)
                        print("{:>10}{o} = {v}".format("",o = option, v = value))
        else:
            for arg in option:
                has_setting = False
                for section in settings.sections():
                    if settings.has_option(section, arg):
                        print(print_tab("[{}]".format(section)))
                        print("{0:>10}{o} = {v}".format("", o = arg, v = settings.get(section, arg)))
                        has_setting = True
                    else:
                        pass
                if not has_setting:
                    print(print_tab("{0:>2}{1} = Undefined".format("", arg)))


    def _print_default_settings(self, option=[]):
        print_tab = lambda x: "{0:>8}{1}".format("", x)

        if not option:
            print("DEFAULT settings:")
            print()

            if PY3:
                for section, options in DEFAULT_CONFIG.items():
                    if not options:
                        pass
                    else:
                        print(print_tab("[{}]".format(section)))
                        for option,value in options.items():
                            print("{0:>10}{o} = {v}".format("", o = option, v = value))

            else:
                for section, options in DEFAULT_CONFIG.iteritems():
                    if not options:
                        pass
                    else:
                        print(print_tab("[{}]".format(section)))
                        for option,value in options.iteritems():
                            print("{0:>10}{o} = {v}".format("", o = option, v = value))
        else:
            for arg in option:
                has_setting = False
                if PY3:
                    for section,options in DEFAULT_CONFIG.items():
                        if arg in options:
                            value = options[arg]
                            print(print_tab("[{}]".format(section)))
                            print("{0:>10}{o} = {v}".format("", o = arg, v = value))
                            has_setting = True
                        else:
                            pass
                else:
                    for section,options in DEFAULT_CONFIG.iteritems():
                        if arg in options:
                            value = options[arg]
                            print(print_tab("[{}]".format(section)))
                            print("{0:>10}{o} = {v}".format("", o = arg, v = value))
                            has_setting = True
                        else:
                            pass

                if not has_setting:
                    print(print_tab("{0:>2}{1} = Undefined".format("", arg)))


    def _set_setting(self, option="", value=""):
        """
        Change a setting and save the new configuration
        """

        settings = self.game.manager.get_config()
        written_setting = False

        if PY3:
            for section,options in DEFAULT_CONFIG.items():
                if option in options:
                    self.game.manager.set_setting(option, value, section)
                    written_setting = True
                else:
                    pass
            if not written_setting:
                self.game.manager.set_setting(option, value)

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

        no args: prints the configuration
        defaults: prints the default configuration values
        get 'option': only prints the single option 'option' and it's value, if assigned
        set 'option' 'value': configures the option 'option' with value 'value'
        """
        if not args:
            self._print_settings()

        else:
            argslist = args.split(" ")
            if 'default' in argslist[0][:7]:
                if argslist[1:]:
                    self._print_default_settings(argslist[1:])
                else:
                    self._print_default_settings()

            elif 'get' in argslist[0]:
                self._print_settings(argslist[1:])

            elif 'set' in argslist[0][:3]:
                if len(argslist) == 3:
                    self._set_setting(argslist[1], argslist[2])
                else:
                    print("wrong number of arguments.")
                    print("Type 'help settings' for information")

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

            elif 'save' in argslist[0]:
                self.game.manager.write_config(self.game.manager.get_config_path())
            else:
                pass

    def do_play(self, args):
        """
        Type 'play' to start the game:

        Whilst playing the user has to guess
        whether the current number is a prime or not
        until the player loses (score is reduced to zero) or ends on a high.

        yes/y: true (the current number is a prime)
        no/n:  false (the current number **isn't** a prime)
        quit/q/stop: quit the game
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
        self.game.manager.save_data(self.game.manager.get_config_path(), self.game.manager.get_highscore_path())
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
    
    def cmd_help(errmsg=""):
        if errmsg:
            eprint(errmsg)
        
        print("Usage:")
        print("no arguments: {0:>11}{1}".format("", "start primegame"))
        print("--conf -conf 'filename': start primegame with")
        print("{0:>25}{1}".format("", "alternative configuration file 'filename'"))
   
    #Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1][:1] == "-": ##only allow - and --flags
            if sys.argv[1] in ('-conf', '--conf'): ##only one cmd arg implemented so far.
                main_cmd = PrimeGameCmd(sys.argv[2])
            else:
                cmd_help("Unknown Argument")
                exit(1)
        else:
            cmd_help("Unknown Argument")
            exit(1)

    else: ##No command line arguments, start with default configuration
        main_cmd = PrimeGameCmd(DEFAULT_CONFIG_PATH)
    
    main_cmd.cmdloop()
