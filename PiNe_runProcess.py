"""
This is the backend run procedure for the PiNe box project.
A call to this class is performed in a parallel thread on selecting the 'Run' button on the main GUI.

Kirubin Pillay, Maria Cobo 13/05/2020
"""

import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from GUIaes import GUIaes
from classes import validate
from verSet import verSet
import logging.handlers
import traceback
import os
from pathlib import Path
import re

def __init__():
    pass