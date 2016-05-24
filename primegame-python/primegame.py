# -*- coding: utf-8 -*-

"""
Primegame module, contains everything needed for the tracking and usage
of the primegame game and it's rules

PrimeGame() = main primegame class, containing all the functions

HOME = the home directory of the current user

DEFAULT_CONFIG_PATH = the default path for the configuration file,
                      amended for use for the primegame game

DEFAULT_HIGHSCORE_PATH = the default path for the highscores file,
                      amended for the use of the primegame game

DEFAULT_CONFIG = the default configuration settings and values,
                 amended for the use for the primegame game

"""



import random
from utils import *
from gamemanager import *
from math import pow

# overwrite default configuration path
HOME = os.path.expanduser("~") # home directory
DEFAULT_CONFIG_PATH = HOME + "/.primegame/primegame.cfg"
DEFAULT_HIGHSCORE_PATH = HOME +  "/.primegame/highscores.csv"

# Add some new default settings
DEFAULT_CONFIG["prime-numbers"] = {
    "min-range" : "1",
    "max-range" : "0",
    "min-score" : "10"
    }
DEFAULT_CONFIG["highscores"]["highscore-file"] = DEFAULT_HIGHSCORE_PATH

class PrimeGame(object):
    """
    Handles all functions and rules needed to play the game,
    but not user interaction

    """


    def __init__(self, config_path=""):
        """
        Initialiser for the class

        arguments:
            config_path = path to file to load configuration from
        """
        # create gamemanager instance to interact with
        self.manager = GameManager(config_path)

        # game business
        self.turn = 0 # Amount of played turns.
        self.correct_count = 0 # Amount of correct guesses
        self.level = 1
        self.score = int(self.manager.get_setting("min-score",
            "prime-numbers")) #Minimum score

        # prime number business
        self.min_range = int(self.manager.get_setting("min-range",
                "prime-numbers")) #minimum range for random numbers
        self.max_range = int(self.manager.get_setting("max-range",
                "prime-numbers")) #maximum range for random numbers
        self.number  = self.new_number()

    def get_min_range(self):
        """
        Returns the minimum range for random numbers,
        defined in the cofiguration settings

        """
        return self.min_range

    def get_max_range(self):
        """
        Returns the maximum range for random numbers,
        defined in the configuration settings

        """
        return self.max_range

    def new_number(self):
        """
        Returns a random number,
        between the range defined in the configuration settings

        If the maximum range is defined as 0
        it'll increase with the rate of 10^level

        """
        max_range = self.get_max_range()
        if max_range == 0:
            max_range = pow(10, self.level)

        return random.randrange(self.get_min_range(), max_range)

    def get_number(self):
        """
        Returns the current randomly generated number

        """
        return self.number

    def _is_prime(self,n):
        """
        Returns True if n is a prime, False otherwise

        """
        answer = True

        if n < 2: # no primes smaller than 2
            answer = False
        elif n == 2: # 2 %2 IS 0, but 2 is a prime
            answer = True
        elif (n % 2) == 0: # even numbers can't be a prime
            answer = False
        else:
            # catch all numbers devideable by odd numbers
            i=3
            while i*i <= n:
                if (n % i) == 0:
                    answer = False
                    break
                i += 2
        return answer

    def guess_prime(self, guess=False):
        """
        checks the guess (as to whether or not
        the current number is a prime) was correct

        arguments:
            guess: guess as to whether the current number is a prime

        returns:
            True:  guess was correct
            False: guess was incorrect

        """
        return guess == self._is_prime(self.get_number())

    def get_turns(self):
        """
        Returns the current turn number

        """
        return self.turn

    def increase_turn(self, amount=1):
        """
        Increases the current turn counter by amount

        arguments:
            amount = amount to raise turns by
                     (default: 1)

        """
        self.turn += amount

    def get_correct_count(self):
        """
        Get the current correct count

        """
        return self.correct_count

    def increase_correct_count(self, amount=1):
        """
        Increases the correct count by amount

        arguments:
            amount = amount to raise turns by
                     (default: 1)

         """
        self.correct_count += amount

    def reset_correct_count(self):
        """
        Resets the current correct counter

        """
        self.correct_count = 0

    def get_level(self):
        """
        Get the current level
        """
        return self.level

    def increase_level(self, amount=1):
        """
        Increases the current level by amount

        arguments:
            amount = amount to raise turns by
                     (default: 1)

        """
        self.level += amount

    def get_score(self):
        """
        Get the current score

        """
        return self.score

    def increase_score(self, amount=1):
        """
        Increases the current score by amount

        arguments:
            amount = amount to raise turns by
                     (default: 1)

        """
        self.score += amount

    def reset_score(self):
        """
        Reset the score to the minimum score defined in the configuration

        """
        self.score = int(self.manager.get_setting("min-score",
            "prime-numbers"))

    def next_turn(self):
        """
        Preforms all the functions required to move to the next turn

        """
        # Generate a new number
        self.number = self.new_number()


        # For every 5 turns
        # if 3 or more turns were correct increase the level
        # and reset the correct count
        if (self.get_turns() % 5) == 0:
            if self.get_correct_count() >= 3:
                self.increase_level()
                self.reset_correct_count()
            else:
        # otherwise, decrease the level if it's not lower than 1
                if self.get_level() > 1:
                    self.increase_level(-1)

        # Increase the turn counter
        self.increase_turn()

    def play_turn(self, answer=False):
        """
        plays a single turn

        Checks the users answer, and depending on whether that was correct
        increases or decreases the score;
        then increases the turn and possibly the level

        arguments:
            answer = the answer provided by the user

        returns:
            a boolean on whether the guess was correct or not

        """
        correct = self.guess_prime(answer)
        # if correct, increase score by the current random number
        # and increase the correct count
        if correct:
            self.increase_score(self.get_number())
            self.increase_correct_count()

        else:
            self.increase_score((self.get_number() * -1))

        self.next_turn()
        return correct

    def __repr__(self):
        """
        Return the current status as a handy string

        """
        return "Turn: {0} | Level: {1} | Score: {2}".format(self.get_turns(),
            self.get_level(), self.get_score())
