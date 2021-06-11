#!/usr/bin/env python3

"""
This is a server scipt to open up a listening port on a macOS system.

Based on the choice of host and port, this can be used to set up a listening server on a mac to feedback outputs
directly from the PiNe box or for closed-loop software testing using the localhost.

Kirubin Pillay 30/05/2020
"""

import socket
import sys

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8000         # Port to listen on (non-privileged ports are > 1023) - same as iXtrend

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

while True:
    data = sock.recv(1024)
    if not data:
        break
    print("received message: {}".format(data))

print('Server no longer listening, press "Ctrl+D" to exit python and restart script')



