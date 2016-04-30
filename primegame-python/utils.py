"""
Utility functions and constants
"""

import sys
import os

NEWLINES={"win32" : '\r\n', 'linux':'\n', 'linux2': '\n', 'macos': '\r\n'}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def clear_alt(num):
    for i in range(num): print 
