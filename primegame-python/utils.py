"""
Utility functions and constants

"""

import sys
import os


##Shorthand to check if script is running in Python 3, only checked once
##Return True if python 3, False otherwise
PY3 = sys.version_info > (3,)

##The various newlines for varying systems, can be used by open() in Python 3
NEWLINES={"win32" : '\r\n', 'linux':'\n', 'linux2': '\n', 'macos': '\r\n'}

def clear():
    """
    Run the system dependant command to clear the terminal

    """
    os.system('cls' if os.name == 'nt' else 'clear')


def clear_alt(num):
    """
    Alternative to clear() prints num amount of newlines

    Portable, but but guesswork way to clear the terminal

    arguments:
        num = amount of newlines to print


    """
    for i in range(num): print()

def eprint(msg):
    """
    Prints a message to stderr

    arguments:
        msg: message to print to stderr

    """
    if PY3:
        eval('print(msg, file=sys.stderr)')
    else:
        sys.stderr.write(msg + "\n")

def get_str(msg=""):
    """
    gets input in the form of a String from the user

    arguments:
        msg = message to use as hint for the user prompt

    returns:
        a String of the user input

    """
    if PY3:
        return str(input(msg))
    else:
        return str(raw_input(msg))

def get_int(msg=""):
    """
    gets input in the form of an Interger from the user

    arguments:
        msg = message to use as hint for the user prompt

    returns:
        user input, converted to an Interger

     """
    if PY3:
        return int(input(msg))
    else:
        return int(raw_input(msg))

def get_bool(msg=""):
    """
    gets input in the form of a Boolean from the user

    arguments:
        msg = message to use as hint for the user prompt

    returns:
        user input, converted to a Boolean

     """
    if PY3:
        answer = str(input(msg))
    else:
        answer = str(raw_input(msg))

    ## translate string into boolean, valid answers are "y", "yes" and "true"
    ## any other answer translates to False
    if answer.lower() in ('yes', 'y', 'true'):
        return True
    else:
        return False
