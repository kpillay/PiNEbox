"""
Main GUI for the PiNE box project
v BETA: interface and functions to add automatic triggers to the vital signs recordings

Kirubin Pillay, Maria Cobo 13/05/2020
"""

import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from GUIaes import GUIaes
from classes import validate
from verSet import verSet
from PiNe_runProcess import PiNeRun
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
import platform
import logging.handlers
import traceback
import os
from pathlib import Path
import re
import time
import threading
import socket


# #### CLASS to initialise the main PiNe GUI ###############################################
class PiNeMain(GUIaes):
    def __init__(self, ver, releaseDate, dev):

        self.ver = ver
        self.releaseDate = releaseDate
        self.dev = dev

        # Check if code is being run on external OS off-Pi, in which case set dummy GPIO pins
        if (platform.system() == 'Darwin') | ((platform.system() == 'Linux') | (platform.system() == 'Windows')):
            Device.pin_factory = MockFactory()

        self.window = tk.Tk()
        self.window.geometry('800x480')
        self.window.resizable(0, 0)
        self.window.title(f'PiNe v{self.ver}')

        self.cont = False
        self.sock = None
        self.__sockTimeout__ = 9  # Allow 9s to connect to IP otherwise throw exception

    # Initialize the system
    def __call__(self):
        # Set the icon
        __p1__ = PhotoImage(file=os.path.join(super().__absPath__, 'pine_icon3.png'))
        self.window.iconphoto(False, __p1__)

        # #### adding frames to the window  #####
        self.frame1 = tk.Frame(self.window, bg=super().__frameBgColour__)
        self.frame1.grid(row=0, column=0, sticky='nsew')

        self.frame2 = tk.Frame(self.window, bg=super().__frameBgColour__)
        self.frame2.grid(row=0, column=1, sticky='nsew')

        self.window.grid_rowconfigure(0, minsize=480, weight=1)
        self.window.grid_columnconfigure(0, minsize=300)
        self.window.grid_columnconfigure(1, minsize=500)

        # adding elements to frame1
        # IP address label
        self.labelIP = tk.Label(self.frame1, bg=super().__frameBgColour__,
                                text='IP address',
                                font=(super().__textFont__, super().__HeadFontSize__), foreground=super().__colourText__)
        self.labelIP.grid(row=1, column=0, padx=(70, 10), sticky=W)

        # port label
        self.labelIP = tk.Label(self.frame1, bg=super().__frameBgColour__,
                                text='port', font=(super().__textFont__, super().__HeadFontSize__),
                                foreground=super().__colourText__)
        self.labelIP.grid(row=3, column=0, padx=(70, 10), sticky=W)

        # IP address entry
        self.varIP = tk.StringVar()
        self.vcmd = self.frame1.register(validate)
        self.ipadd = tk.Entry(self.frame1, textvariable=self.varIP, width=14,
                              highlightthickness=0, highlightcolor=super().__frameBgColour__, bg=super().__colourText__,
                              highlightbackground=super().__frameBgColour__, borderwidth=0,
                              font=(super().__textFont__, super().__HeadFontSize__), fg=super().__frameBgColour__,
                              validate='key', validatecommand=(self.vcmd, '%P'))
        self.ipadd.grid(row=0, column=0, padx=70, pady=(100, 5))

        # port entry
        self.varPort = tk.StringVar()
        self.port = tk.Entry(self.frame1, textvariable=self.varPort, width=8, highlightthickness=0,
                             highlightcolor=super().__frameBgColour__, bg=super().__colourText__,
                             highlightbackground=super().__frameBgColour__, borderwidth=0,
                             font=(super().__textFont__, super().__HeadFontSize__), fg=super().__frameBgColour__)
        self.port.grid(row=2, column=0, padx=70, pady=(50, 5), sticky=W)

        # adding elements to frame2
        super().__renderLogo__(self.frame2)
        self.instr_text = Label(self.frame2, bg=super().__frameBgColour__,
                                text=f'Released on {self.releaseDate} \n'
                                     f'Developed by {self.dev}',
                                font=(super().__textFont__, super().__textFontSize__), fg=super().__colourSubHead__)

        self.instr_text.pack(side=TOP)

        # Create message label
        self.labelMess = tk.Label(self.frame2, bg=super().__frameBgColour__,
                                  text='', font=(super().__textFont__, super().__HeadFontSize__),
                                  foreground=super().__colourText__)
        self.labelMess.pack(side=LEFT)

        # Add button frame
        self.buttonFrame = Frame(self.frame1, highlightthickness=0, borderwidth=0, background=super().__frameBgColour__)
        self.buttonFrame.grid(row=5, column=0, padx=70, pady=(50, 5), sticky=W)

        # Add RUN button
        self.runImage = super().__renderImageOnly__(50, 50, 'start_icon_grey.png')
        self.runButton = Button(self.buttonFrame, image=self.runImage,
                                compound=LEFT,  highlightthickness=0, borderwidth=0, highlightbackground='black',
                                command=self.__initSocket_callback__)
        self.runButton.pack(side=LEFT, padx=4)

        # Add STOP/RESET button
        self.stopImage = super().__renderImageOnly__(50, 50, 'stop_icon_grey.png')
        self.stopButton = Button(self.buttonFrame, image=self.stopImage, compound=LEFT,  highlightthickness=0,
                                 borderwidth=0, highlightbackground='black', state=DISABLED,
                                 command=self.__initStop_callback__)
        self.stopButton.pack(side=LEFT, padx=4)

        # Add QUIT button
        self.quitImage = super().__renderImageOnly__(50, 50, 'quit_icon_grey.png')
        self.quitButton = Button(self.buttonFrame, image=self.quitImage, compound=LEFT,  highlightthickness=0,
                                 borderwidth=0, highlightbackground='black')
        self.quitButton.pack(side=LEFT, padx=4)

        # Set logic state, default IP and port values from text file
        IPfile = open('setup.txt', 'r')

        # Load logic state
        __logicState__ = str.rstrip(IPfile.readline())
        if (__logicState__[0:5] == 'LOGIC') & ((__logicState__[6:] == 'HIGH') | (__logicState__[6:] == 'LOW')):
            self.__logicState__ = __logicState__[6:]
        else:
            self.varIP.set('-')
            self.varPort.set('-')
            self.labelMess.config(text='Fatal Error: LOGIC state in setup.txt', foreground=super().__colourText__)
            self.runButton.config(state=DISABLED)
            return

        # Load LED duration value
        __LEDduration__ = str.rstrip(IPfile.readline())
        if (__LEDduration__[0:11] == 'LEDduration') & (__LEDduration__[12:] != ''):
            self.__LEDduration__ = float(__LEDduration__[12:])
        else:
            self.varIP.set('-')
            self.varPort.set('-')
            self.labelMess.config(text='Fatal Error: LEDduration in setup.txt', foreground=super().__colourText__)
            self.runButton.config(state=DISABLED)
            return

        # Load default IP address
        __IPaddr__ = str.rstrip(IPfile.readline())
        if (__IPaddr__[0:2] == 'IP') & (__IPaddr__[3:] != ''):
            self.varIP.set(__IPaddr__[3:])
        else:
            self.varIP.set('-')
            self.varPort.set('-')
            self.labelMess.config(text='Fatal Error: IP address in setup.txt', foreground=super().__colourText__)
            self.runButton.config(state=DISABLED)
            return

        # Load default IP address
        __port__ = str.rstrip(IPfile.readline())
        if (__port__[0:4] == 'PORT') & (__port__[5:] != ''):
            self.varPort.set(__port__[5:])
        else:
            self.varIP.set('-')
            self.varPort.set('-')
            self.labelMess.config(text='Fatal Error: PORT value in setup.txt', foreground=super().__colourText__)
            self.runButton.config(state=DISABLED)
            return

        # Set the broken pipe error check
        self.pipeCheck = tk.BooleanVar(False)
        self.pipeCheck.trace("w", self.__pipeBreakSafe__)

    # Initiate socket connection on selecting Run callback
    def __initSocket_callback__(self):

        # Disable run button to avoid initialising multiple threads
        self.runButton.config(state=DISABLED)

        # Display status message
        self.labelMess.config(text='Establishing connection...', foreground=super().__colourText__)

        # Enable stop button
        self.stopButton.config(state=NORMAL)

        # Start countdown on separate thread
        self.cont = True
        self.threadCountdown = threading.Thread(target=self.__countdown__)
        self.threadCountdown.start()

        # Initialize socket connection and check if successful
        self.__host__ = self.varIP.get()
        self.__port__ = int(self.varPort.get())

        self.threadSock = threading.Thread(target=self.__initSocket__)
        self.threadSock.start()

    # Initiate stop sequence if system has started running
    def __initStop_callback__(self):

        # Stop countdown if still running (also safely ends the thread)
        self.cont = False

        # Destroy countdown and delete label message text
        if hasattr(self, 'countdownMess'):               # May have been destroyed during threading beforehand
            self.countdownMess.destroy()
        self.labelMess.config(text='', foreground=super().__colourText__)

        # Close open socket (if established)
        if self.sock is not None:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)    # Fail-safe in case server has been shut down first
            except OSError:
                pass
            self.sock.close()
            self.sock = None

        # Disable stop button
        self.stopButton.config(state=DISABLED)

        # Enable run button
        self.runButton.config(state=NORMAL)

        # Stop UDP transmission
        self.triggerSend.cancel = True

    # Initiate stop sequence if system has started running
    # def __initQuit_callback__(self):

    # Process to deal with closing safely when unexpected broken pipe occurs
    def __pipeBreakSafe__(self, *_):
        self.__initStop_callback__()
        self.labelMess.config(text='Connection Lost. Check server & retry.', foreground=super().__colourText__)

    # Perform a countdown while establishing connection (until externally cancelled)
    def __countdown__(self):

        # Create countdown label
        self.countdownMess = tk.Label(self.frame2, bg=super().__frameBgColour__,
                                      text='', font=(super().__textFont__, super().__HeadFontSize__),
                                      foreground=super().__colourText__)
        self.countdownMess.pack(side=LEFT)

        stTime = self.__sockTimeout__
        t = stTime
        while (t >= 0) & self.cont:
            self.countdownMess.config(text=str(t))
            time.sleep(1)
            t -= 1

    # Set up the initial socket connection with the server (threaded function)
    def __initSocket__(self):

        # Initialise socket and set up timeout limit for connecting
        self.sock = socket.socket()
        self.sock.settimeout(self.__sockTimeout__+1)

        try:
            self.sock.connect((self.__host__, self.__port__))

        # Occurs if a connection could not be established (often because IP or port is incorrect)
        except socket.timeout:

            # Stop countdown and reset
            self.cont = False
            time.sleep(1)       # 'Hack' to ensure while loop in countdown is exited before destroying attributes

            # Destroy countdown and change label message text to unsuccessful
            self.countdownMess.destroy()
            self.labelMess.config(text='Connection Timed Out.', foreground=super().__colourText__)

            # Disable stop button
            self.stopButton.config(state=DISABLED)

            # Enable run button
            self.runButton.config(state=NORMAL)

            return

        # Occurs if server is not listening at the specified port
        except ConnectionRefusedError:

            # Stop countdown and reset
            self.cont = False
            time.sleep(1)

            # Destroy countdown and change label message text to unsuccessful
            self.countdownMess.destroy()
            self.labelMess.config(text='Connection Refused.', foreground=super().__colourText__)

            # Disable stop button
            self.stopButton.config(state=DISABLED)

            # Enable run button
            self.runButton.config(state=NORMAL)

            return

        # If connection successful, system then can only be exited by stop button callback
        # Stop countdown if still running
        self.cont = False
        time.sleep(1)

        # Overwrite text file with new correct values
        with open('setup.txt', 'w') as IPfile:
            IPfile.write(f'LOGIC={self.__logicState__}\nLEDduration={self.__LEDduration__}\n'
                         f'IP={self.varIP.get()}\nPORT={self.varPort.get()}')

        # Create 'success' message label
        self.countdownMess.destroy()
        self.labelMess.config(text='Connection successful.', foreground=super().__colourGood__)

        # Send initial connection message
        initMess = 'PiNeConnected'
        self.sock.sendall(PiNeRun.sendiXmess(initMess))

        # Instantiate PiNeRun instance and begin trigger listening (threaded)
        self.triggerSend = PiNeRun(self.sock, self.pipeCheck, logicState=self.__logicState__,
                                   LEDduration=self.__LEDduration__)
        self.threadTrigg = threading.Thread(target=self.triggerSend)
        self.threadTrigg.start()


# Initialise and run tkinter loop
def main(ver, releaseDate, dev):

    if getattr(sys, 'frozen', False):
        __absPath__ = str(Path.home())
    else:
        __absPath__ = os.path.dirname(os.path.abspath(__file__))

    # Run the GUI
    # try:
        app = PiNeMain(ver, releaseDate, dev)
        app()
    # except Exception as inst:
    #     messagebox.showerror('UNKNOWN ERROR', 'UNKNOWN ERROR: Please contact system administrator')
    #     sys.exit()

    app.window.mainloop()


# #### MAIN to run application ########################################################################################
if __name__ == '__main__':
    main()
