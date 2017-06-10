#!/usr/bin/env python
"""
    libutils.colours
    ================

    Convenient colour functions
"""
from escape_codes import escape_codes


__all__ = (
    'happy', 'sad', 'bold', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan',
    'black', 'white', 'grey'
)


def colourise(colour, msg='', return_colour=None):
    """ Generic function to colourise a message with an escape code. """
    if return_colour is None:
        return colour + msg + escape_codes['reset']
    else:
        return colour + msg + escape_codes['reset'] + return_colour


def bold(msg): return colourise(escape_codes['bold'], msg)
def red(msg): return colourise(escape_codes['red'], msg)
def green(msg): return colourise(escape_codes['green'], msg)
def yellow(msg, return_colour=None): return colourise(escape_codes['yellow'], msg, return_colour)
def blue(msg): return colourise(escape_codes['blue'], msg)
def purple(msg): return colourise(escape_codes['purple'], msg)
def cyan(msg): return colourise(escape_codes['cyan'], msg)
def black(msg): return colourise(escape_codes['black'], msg)
def white(msg): return colourise(escape_codes['white'], msg)
def grey(msg): return colourise(escape_codes['grey'], msg)
def happy(): return (green('\nLooks good from here!\n'))
def sad(): return (red(r'''
          ___           ___
         /  /\         /__/\
        /  /::\        \  \:\
       /  /:/\:\        \__\:\
      /  /:/  \:\   ___ /  /::\
     /__/:/ \__\:\ /__/\  /:/\:\
     \  \:\ /  /:/ \  \:\/:/__\/
      \  \:\  /:/   \  \::/
       \  \:\/:/     \  \:\
        \  \::/       \  \:\
         \__\/         \__\/
          ___           ___           ___           ___
         /__/\         /  /\         /  /\         /  /\     ___
         \  \:\       /  /::\       /  /:/_       /  /:/_   /__/\
          \  \:\     /  /:/\:\     /  /:/ /\     /  /:/ /\  \  \:\
      _____\__\:\   /  /:/  \:\   /  /:/ /:/_   /  /:/ /::\  \  \:\
     /__/::::::::\ /__/:/ \__\:\ /__/:/ /:/ /\ /__/:/ /:/\:\  \  \:\
     \  \:\~~\~~\/ \  \:\ /  /:/ \  \:\/:/ /:/ \  \:\/:/~/:/   \  \:\
      \  \:\  ~~~   \  \:\  /:/   \  \::/ /:/   \  \::/ /:/     \__\/
       \  \:\        \  \:\/:/     \  \:\/:/     \__\/ /:/          __
        \  \:\        \  \::/       \  \::/        /__/:/          /__/\
         \__\/         \__\/         \__\/         \__\/           \__\/

         Opps. Something seems to have gone wrong!
         You should probably take a look at that.
    '''))
