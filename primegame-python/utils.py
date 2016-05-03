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
        print(msg, file-sys.stderr)
    else:
        sys.stderr.write(msg)


