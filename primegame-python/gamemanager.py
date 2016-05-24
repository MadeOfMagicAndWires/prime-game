# -*- coding: utf-8 -*-

"""
A generic game manager that handles the reading and writing
of configuration and highscores

GameManager = the main gamemanager class, containing all the functions
DEFAULT_CONFIG_PATH = the default path for the configuration file
DEFAULT_HIGHSCORE_PATH = the default path for the highscores file
DEFAULT_CONFIG = the default configuration settings and values
DEFAULT_HIGHSCORES = default highscores to initiate the scoreboard with

"""



import os
import csv
from utils import *

#configparser is named differently in python 2 and 3
if PY3:
    import configparser as Config
else:
    import ConfigParser as Config

DEFAULT_CONFIG_PATH="data/gamemanager.cfg" # Default configuration path to load
DEFAULT_HIGHSCORE_PATH="data/highscores.csv" # Default highscore path to use in configuration

# Default configuration settings and values
DEFAULT_CONFIG={'general': {},
                'highscores':
                    {
                        'highscore-file' : DEFAULT_HIGHSCORE_PATH,
                        'max-highscores': "10"
                    }
                }

# Default highscore values
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

       arguments:
        config_path = path to a file
                      to load the configuration
                      settings from

        """

        self.config_path = config_path         # Configuration file
        self.config     = self.load_config() # Confuration settings
        self.highscore_path = self.get_setting("highscore-file",
                section="highscores")        # Highscore file
        self.max_highscores = int(self.get_setting('max-highscores',
            section="highscores"))# Maximum ammount of highscores
        self.highscores = self.load_highscores() # Highscores dict

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
            # make parent directory if non-existent,
            # open new file in directory
            if not os.path.exists(os.path.dirname(self.get_config_path())):
                os.makedirs(os.path.dirname(self.get_config_path()))
            config.read(self.get_config_path())
        except (FileNotFoundError, IOError) as e:
            eprint(e)

        if not config.sections(): # Configuration is empty
            eprint("Configuration was not found, moving to defaults")
            config = self.default_settings(config)

        return config


    def default_settings(self, config=None):
        """
        Sets the configuration to the default settings

        arguments:
            config = empty ConfigParser object

        returns:
            a ConfigParser object containing the values
            defined in DEFAULT_CONFIG

        """

        if not config:
            config = Config.ConfigParser()

        # python 2 doesn't have the read_dict() function
        if PY3:
            config.read_dict(DEFAULT_CONFIG)
        else:
            for section,options in DEFAULT_CONFIG.iteritems():
                config.add_section(section)
            for option,value in options.iteritems():
                config.set(section, option, value)

        return config

    def get_config(self):
        """
        Returns ConfigParser object to read

        """
        return self.config

    def get_setting(self,setting, section="general"):
        """
        Looks up the value of a configuration setting

        arguments:
            setting = the setting to retrieve from the configuration
            section = the section to look in for the setting
                      (default: 'general')

        returns:
            the value of a configuration

        """
        try: # Check if setting is available in self.config
            return self.config.get(section, setting)
        except Config.NoSectionError: # else get it from DEFAULT_CONFIG
            return DEFAULT_CONFIG[section][setting]

    def set_setting(self,setting, value, section="general"):
        """
        Sets the value for a configuration setting

        arguments:
            setting = the setting to set in the configuration
            value   = the value to set the setting to
            section = the section to put the setting in
                      (default: 'general')

        """
        try:
            # Check if section is present in self.config
            # and set the new setting/value
            self.config.set(section, setting, str(value))
        except Config.NoSectionError:
            # Otherwise, first add the section
            self.config.add_section(section)
            self.config.set(section, setting, str(value))

        self.write_config(self.get_config_path())

    def write_config(self, file_path=""):
        """
        Writes the configuration to a file

        arguments:
            file_path = the file to write the configuration to

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

        The file it reads from is configured in the configuration file
        Returns a dictionary with scores as the key, and names as value

        """
        highscores = dict()

        try:
            # if the parent folder doesn't exist yet, create it
            if not os.path.exists(os.path.dirname(self.get_highscore_path())):
                os.makedirs(os.path.dirname(self.get_highscore_path()))
            with open(self.highscore_path, 'r') as f:
                csvalues = csv.reader(f)

                try:
                    # function for the next line is named differently
                    # in python 3 and python 2
                    if PY3:
                        csvalues.__next__()
                    else:
                        csvalues.next()
                except StopIteration: #only raised when csvalues is empty
                    highscores = DEFAULT_HIGHSCORES

                for row in csvalues:
                    # dictionary is in the format of highscores[score] = name
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

        arguments:
            new_score = the new score to check highscores against

        returns:
            True if new_score is larger than the smallest score
            present in the highscores dictionary, False otherwise

        """

        # check if new score is equal or bigger than the smallest highscore
        return new_score >= min(self.highscores.keys())

    def add_highscore(self, new_highscore, name=""):
        """
        Add a new highscore to the list of highscores

        arguments:
            new_highscore = the new score to add

        """

        # if no name is given than use "-" as the name
        if not name:
            name = "-"

        # only allow a top x highscores, delete the old one
        minimum_highscore= min(self.highscores.keys())
        if len(self.highscores) >= self.max_highscores:
            del self.highscores[minimum_highscore]

        self.highscores[new_highscore] = name
        self.write_highscores(self.get_highscore_path())

    def write_highscores(self, file_path=""):
        """
        Write new highscores to a file.

        Writes the highscores from the dictionary in a CSV format
        With names as the first field, name as the second.

        arguments:
            file_path = the file to write the hihgscores to
        """

        print("Saving new highscores...")
        try:
            with open(file_path, 'w') as highscoresf:
                # Write a CSV file containing every highscore
                #in a score, name format
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

        arguments:
            config_path    = path to file to write the configuration to
            highscore_path = path to file to write the highscores to

        """

        # Write files if they don't already exist
        try:
            open(config_path,'x')
            self.write_config(config_path)
            open(highscore_path, 'x')
            self.write_highscores(highscore_path)
        except FileExistsError:
            # If the file already exists check whether they're not empty
            # and if so, write the data anyway
            if os.stat(config_path).st_size == 0:
                self.write_config(config_path)
            if os.stat(highscore_path).st_size == 0:
                self.write_highscores(_highscore_path)


