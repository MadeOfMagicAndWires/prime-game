# -*- coding: utf-8 -*-

import random
from utils import *
from gamemanager import *
from math import pow

##overwrite default configuration path
HOME = os.path.expanduser("~")
DEFAULT_CONFIG_PATH = HOME + "/.primegame/primegame.cfg"
DEFAULT_HIGHSCORE_PATH = HOME +  "/.primegame/highscores.csv"

##Add some default settings
DEFAULT_CONFIG["prime-numbers"] = {
    "min-range" : "1",
    "max-range" : "0",
    "min-score" : "10"
    }
DEFAULT_CONFIG["highscores"]["highscore-file"] = DEFAULT_HIGHSCORE_PATH

class PrimeGame(object):
    """
    Handles all functions and rules needed to play the game,
    but not interaction
    """


    def __init__(self, config_path=""):
        """
        Initialiser for the class
        """
        ##create gamemanager instance to interact with
        self.manager = GameManager(config_path)

        ##game business
        self.turn = 0 ##Amount of played turns.
        self.correct_count = 0
        self.level = 1
        self.score = int(self.manager.get_setting("min-score",
            "prime-numbers")) #Minimum score

        ##prime number business
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

        if n < 2:
            answer = False
        if (n % 2) == 0:
            answer = False
        else:
            i=3
            while i*i <= n:
                if (n % i) == 0:
                    answer = False
                    break
                i += 2
        return answer

    def guess_prime(self, guess=False):
        """
        Returns True if the guess was correct, False otherwise
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
        """
        self.correct_count += amount

    def get_level(self):
        """
        Get the current level
        """
        return self.level

    def increase_level(self, amount=1):
        """
        Increases the current level by amount
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
        ##Generate a new number
        self.number = self.new_number()

        '''
        For every 5 turns
        if 3 or more turns were correct increase the level
        and reset the correct count
        '''
        if (self.get_turns() % 5) == 0:
            if self.get_correct_count() >= 3:
                self.increase_level()
                self.increase_correct_count((self.get_correct_count())*-1)
            else:
                if self.get_level() > 1:
                    self.increase_level(-1)

        ##Increase the turn counter and print the current state
        self.increase_turn()

    def play_turn(self, answer=False):
        """
        Everything needed to play a single turn
        using the answer provided
        """
        correct = self.guess_prime(answer)
        ##if correct, increase score by the current random number
        ##and increase the correct count
        if correct:
            self.increase_score(self.get_number())
            self.increase_correct_count()

        else:
            self.increase_score((self.get_number() * -1))

        self.next_turn()
        return correct

    def __repr__(self):
        """
        Return the current status
        """
        return "Turn: {0} | Level: {1} | Score: {2}".format(self.get_turns(),
            self.get_level(), self.get_score())

def notprime(n):
    """If integer isn't a prime, what is it then?"""
    for x in range(3, int(n**0.5)+1, 2):

        if n % x == 0:

            return str(n) + ' is the product of ' + str(x) + ' * ' + str(n/x)



def play():

    """Play the game.

    answer 'q' or 'quit' to quit
    """

    line = "----------------------"
    correct_count = True
    rand_max=10
    number = random.randrange(1,rand_max,2)
    prime = isprime(number)
    level = 1
    score = 0
    turn = 0
    limit = 2

    clear.clear()
    print("\t\t\t\t\tStart!\n\n")

    while correct_count == True:

        print(number, '\n')
        answer=str(raw_input("Is this a prime y/n? "))
        if answer not in ('q', 'n', 'y', '0', 'quit', 'no', 'ye', 'yes', 's', 'stop'):
            print("Please answer in yes or no\n")
            continue
        if answer in ('y', 'ye', 'yes'):
            answer =  True
        if answer in ('n', 'no'):
            answer = False
        if answer in ('s', 'stop', '0'):
            return score
            break
        if answer in ('q', 'quit'):
            exit()

        if answer == prime:
            clear.clear()
            score = score + number
            print("Correct!\n")
            print(line+line)
            print("Your score is: " + str(score))
            print(line+line, "\n")
            turn = turn+1
            if turn >= limit:
                limit = 5*level
                level = level+1
                rand_max = rand_max*10
                print("Level " + str(level) + "!" + "\n")


            correct_count = True
            number = random.randrange(1,rand_max,2)
            prime = isprime(number)

        elif answer != prime:
            correct_count == False
            score = 0
            turn = 0
            level = level/2
            rand_max=rand_max/2
            limit = limit/2

            clear.clear()
            if notprime(number) != None:
                print("\nIncorrect_count! ", notprime(number))

            else:
                print("\nIncorrect_count! ")

            print(line+line)
            print("Your score is: " + str(score))
            print(line+line, "\n")
            print("Level " + str(level) + "!" + "\n")

            number = random.randrange(1,rand_max,2)
            prime = isprime(number)


if __name__ == "__main__":
    import sys
    game = PrimeGame(DEFAULT_CONFIG_PATH)

    if PY3:
        for x in range(0,10):
            print("Current number: {}".format(game.get_number()))
            print(game.play_turn(False))
            if game.get_score() <= 0:
                print("Game over!")
                break
    else:
        for x in xrange(0,10):
            print(game.get_number())
            print(game.play_turn(False))
            if game.get_score() <= 0:
                print("Game over!")
                break
