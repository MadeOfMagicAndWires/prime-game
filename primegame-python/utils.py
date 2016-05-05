"""
Utility functions and constants
"""

import sys
import os


PY3 = sys.version_info > (3,)
NEWLINES={"win32" : '\r\n', 'linux':'\n', 'linux2': '\n', 'macos': '\r\n'}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def clear_alt(num):
    for i in range(num): print

def eprint(msg):
    if PY3:
        eval('print(msg, file=sys.stderr)')
    else:
        sys.stderr.write(msg + "\n")

def get_str(msg=""):
    if PY3:
        return str(input(msg))
    else:
        return str(raw_input(msg))

def get_int(msg=""):
    if PY3:
        return int(input(msg))
    else:
        return int(raw_input(msg))

def get_bool(msg=""):
    if PY3:
        answer = str(input(msg))
    else:
        answer = str(raw_input(msg))

    if answer.lower() == "true" \
    or answer.lower() == "yes":
        return True
    else:
        return False
