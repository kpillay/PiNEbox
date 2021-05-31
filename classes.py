"""
Class to set a validation format for the IP address label

Maria Cobo 30.12.2020
"""

from tkinter import *
from GUIaes import GUIaes


def validate(P):
    # Permissable IP address formats
    test = re.compile('(^\d{0,3}$|^\d{1,3}\.\d{0,3}$|^\d{1,3}\.\d{1,3}\.\d{0,3}$|^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{0,3}$)')
    if test.match(P):
        return True
    else:
        return False
