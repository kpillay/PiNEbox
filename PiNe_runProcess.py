"""
This is the backend run procedure for the PiNe box project.
A call to this class is performed in a parallel thread on selecting the 'Run' button on the main GUI.

Class PiNErun performs general UDP messaging between PiNe box client and iXTrend server.
Assumes a socket connection is already established and passes in a socket tuple.

Kirubin Pillay, Maria Cobo 13/05/2020
"""

import logging.handlers
import traceback
import os
from pathlib import Path
import re


class PiNeRun:

    def __init__(self, sockTup):
        pass

    # Send an iXTrend-formatted message
    @staticmethod
    def sendiXmess(MESSAGE):

        # Compile UDP message
        start = bytes([0 for i in range(0, 8)])
        end = bytes([0 for i in range(0, 8)])
        message_len = bytes([len(MESSAGE)])
        my_str_as_bytes = str.encode(MESSAGE)
        iX_message = start + end + message_len + my_str_as_bytes

        return iX_message

