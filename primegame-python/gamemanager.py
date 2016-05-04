#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import csv
import utils

if utils.PY3: ##if running python3:
    import configparser as Config
else:
    import ConfigParser as Config

COMMANDS={
        'highscores': 'highscores',
        'highscores-alias': 'high',
        'play': 'play',
        'play-alias': 'p',
        'quit': 'quit',
        'quit-alias': 'q',
        'help': 'help',
        'help-alias': 'h',
        'settings' : 'settings',
        'settings-alias' : 'config'
        }


DEFAULT_HIGHSCOREPATH="data/highscores.csv"
DEFAULT_CONFIGPATH="data/gamemanager.cfg"

DEFAULT_CONFIG={'general': {},
                'highscores':
                    {
                        'highscore-file' : DEFAULT_HIGHSCOREPATH,
                        'max-highscores': "10"
                    }
                }


DEFAULT_HIGHSCORES={
        6000 : 'Vax',
        3000 :'Vex',
        2000 :'Pyke',
        10000 :'Grog',
        200 : 'Percy',
        400 : 'Keyleth',
        0 :'Tiberius',
        500 : 'Scanlan',
        9000 : 'Mercer'
        }

class GameManager(object):
    """
    Manages generic game aspects like reading configurations,
    keeping track of highscores, and a basic menu.
    """

    def __init__(self, configpath=""):
        """
        Initialisation of the class instance.
        """

        self.configpath = configpath         ##Configuration file
        self.config     = self.load_config() ##Confuration settings
        self.highscorespath = self.get_setting("highscore-file",
                section="highscores")        ##Highscore file
        self.max_highscores = int(self.get_setting('max-highscores',
            section="highscores"))##Maximum ammount of highscores
        self.highscores = self.load_highscores() ##Highscores dict

    def get_configpath(self):
        """
        Returns the path to the configuration file
        """
        return self.configpath


    def load_config(self):
        """
        Reads and returns the configuration settings from an .ini file
        """
        config = Config.ConfigParser()

        try:
            config.read(self.get_configpath())
        except IOError:
            print(e)

        if not config.sections():
            utils.eprint("Configuration was not found, moving to defaults")

            if utils.PY3: ##runing python3
                config.read_dict(DEFAULT_CONFIG)
            else: ##python2 doesn't have read_dict()
                for section,options in DEFAULT_CONFIG.iteritems():
                    config.add_section(section)
                    for option,value in options.iteritems():
                        config.set(section, option, value)

        return config

    def get_setting(self,setting, section="general"):
        """
        Returns the value of a configuration setting
        """
        try:
            return self.config.get(section, setting)
        except Config.NoSectionError:
            return DEFAULT_CONFIG[section][setting]

    def set_setting(self,setting, value, section="general"):
        """
        Sets the value for a configuration setting
        """
        try:
            self.config.set(section, setting, str(value))
        except Config.NoSectionError:
            self.config.add_section(section)
            self.config.set(section, setting, str(value))

        self.write_config()

    def write_config(self):
        """
        Writes the configuration to the same configuration file it read from
        """
        print("Saving configuration")
        try:
            with open(self.get_configpath(), 'w') as configfile:

                self.config.write(configfile)
                print("Success!")

        except IOError as e:
            utils.eprint("Could not save configuration to file {}."
                    .format(self.get_configpath()))
            utils.eprint(e)

    def get_highscorepath(self):
        """
        Returns the path to the file containing highscores.
        """
        return self.highscorepath

    def get_highscores(self):
        """
        Returns the highscores as a dictionary
        """
        return self.highscores

    def load_highscores(self):
        """
        Loads existing highscores from the highscorefile
        defined in the configuration file

        Returns the data as a dictionary,
        with name as the key and the score as the value
        """
        highscores = dict()

        try:
            with open(self.highscorespath, 'a+') as ftest:
                pass
        except IOError as e:
            print(e)
            highscores = DEFAULT_HIGHSCORES

        with open(self.highscorespath, 'a+') as f:
            csvalues = csv.reader(f)

            try:
                if utils.PY3: ##if running python 3
                    csvalues.__next__()
                else:
                    csvalues.next()
            except StopIteration:
                highscores = DEFAULT_HIGHSCORES

            highscores = dict()
            for row in csvalues:
                highscores[int(row[0])] = row[1]

        if not highscores:
            highscores = DEFAULT_HIGHSCORES

        return highscores


    def check_highscore(self, new_score):
        """
        Check if the new score is a new highscore
        """
        ##check if new score is equal or bigger than the smallest highscore
        return new_score >= min(self.highscores.keys())

    def add_highscore(self, new_highscore, name):
        """
        Add a new highscore to the list of highscores
        """

        ##only allow a top x highscores, delete the old one
        minimum_highscore= min(self.highscores.keys())
        if len(self.highscores) >= self.max_highscores:
            del self.highscores[minimum_highscore]

        self.highscores[new_highscore] = name
        self.write_highscores()

    def write_highscores(self):
        """
        Write new highscores to the file specified in the configuration file
        """

        print("Saving highscores...".format('right aligned'))
        try:
            with open(self.highscorespath, 'w') as highscoresf:

                fieldnames = ('score', 'name')
                writer = csv.DictWriter(highscoresf, fieldnames)

                writer.writeheader()

                sortkey= lambda x:x[1]

                for key in sorted(self.highscores.keys(), reverse=True):
                    value = self.highscores[key]
                    writer.writerow({fieldnames[0]:key,
                        fieldnames[1]: value})
                print("Success!")

        except IOError as e:
            eprint("Could not save highscores to file: {}".format(
                self.get_highscorespath()))
            print(e)
