# -*- coding: utf-8 -*-


import os
import csv
from utils import *

if PY3: ##if running python3:
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
DEFAULT_CONFIG_PATH="data/gamemanager.cfg"

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

    def __init__(self, config_path=""):
        """
        Initialisation of the class instance.
        """

        self.config_path = config_path         ##Configuration file
        self.config     = self.load_config() ##Confuration settings
        self.highscore_path = self.get_setting("highscore-file",
                section="highscores")        ##Highscore file
        self.max_highscores = int(self.get_setting('max-highscores',
            section="highscores"))##Maximum ammount of highscores
        self.highscores = self.load_highscores() ##Highscores dict

    def get_config_path(self):
        """
        Returns the path to the configuration file
        """
        return self.config_path


    def load_config(self):
        """
        Reads and returns the configuration settings from an .ini file
        """
        config = Config.ConfigParser()

        try:
            if not os.path.exists(os.path.dirname(self.get_config_path())):
                os.makedirs(os.path.dirname(self.get_config_path()))
            config.read(self.get_config_path())
        except (FileNotFoundError, IOError) as e:
            print(e)

        if not config.sections():
            eprint("Configuration was not found, moving to defaults")
            config = self.default_settings(config)

        return config


    def default_settings(self, config):
        if PY3: ##runing python3
            config.read_dict(DEFAULT_CONFIG)
        else: ##python2 doesn't have read_dict()
            for section,options in DEFAULT_CONFIG.iteritems():
                config.add_section(section)
            for option,value in options.iteritems():
                config.set(section, option, value)

        return config

    def get_config(self):
        return self.config

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

        self.write_config(self.get_config_path())

    def write_config(self, file_path=""):
        """
        Writes the configuration to the same configuration file it read from
        """
        try:
            print("Saving new configuration...")
            with open(file_path, 'w') as configfile:
                self.config.write(configfile)
                print("Success!")
        except IOError as e:
            eprint("Could not save configuration to file {}."
                    .format(file_path))
            eprint(e)

    def get_highscore_path(self):
        """
        Returns the path to the file containing highscores.
        """
        return self.highscore_path

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
            if not os.path.exists(os.path.dirname(self.get_highscore_path())):
                os.makedirs(os.path.dirname(self.get_highscore_path()))
            with open(self.highscore_path, 'r') as f:
                csvalues = csv.reader(f)

                try:
                    if PY3: ##if running python 3
                        csvalues.__next__()
                    else:
                        csvalues.next()
                except StopIteration:
                    highscores = DEFAULT_HIGHSCORES

                for row in csvalues:
                    highscores[int(row[0])] = row[1]

        except (FileNotFoundError, IOError) as e:
            print(e)
            highscores = DEFAULT_HIGHSCORES

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
        self.write_highscores(self.get_highscore_path())

    def write_highscores(self, file_path=""):
        """
        Write new highscores to the file specified in the configuration file
        """

        print("Saving new highscores...")
        try:
            with open(file_path, 'w') as highscoresf:

                fieldnames = ('score', 'name')
                writer = csv.DictWriter(highscoresf, fieldnames)

                writer.writeheader()

                sortkey= lambda x:x[1]

                for key in sorted(self.highscores.keys(), reverse=True):
                    value = self.highscores[key]
                    writer.writerow({fieldnames[0]:key,
                        fieldnames[1]: value})
                print("Success!")

        except (IOError) as e:
            eprint("Could not save highscores to file: {}".format(
                file_path))
            print(e)

    def save_data(self, config_path="", highscore_path=""):
        """
        Checks if the configuration- and highscore files already exist or need to be saved
        """

        ##Write files if they don't already exist
        try:
            open(config_path,'x')
            self.write_config(config_path)
            open(highscore_path, 'x')
            self.write_highscores(highscore_path)
        except FileExistsError:
            ##If the file already exists check if the is not empty
            if os.stat(config_path).st_size == 0:
                self.write_config(config_path)
            if os.stat(highscore_path).st_size == 0:
                self.write_highscores(_highscore_path)


