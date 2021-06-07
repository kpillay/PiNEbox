"""
Main GUI for the PiNE box project
v BETA: interface and functions to add automatic triggers to the vital signs recordings

Maria Cobo, Kirubin Pillay 13/05/2020
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


# #### CLASS to initialise the main PiNe GUI ####### ####### ####### ####### ####### ####### ####### ####### #######
class PiNeMain(GUIaes):
    def __init__(self, ver, releaseDate, dev, logger):

        self.logger = logger
        self.ver = ver
        self.releaseDate = releaseDate
        self.dev = dev
        self.messType = 'UDP'
        self.__logicState__ = 'HIGH'

        self.window = tk.Tk()
        self.window.resizable(0, 0)
        self.window.title(f'PiNe v{self.ver}')

        # Check if code is being run on external OS off-Pi (for simulation), in which case set dummy GPIO pins
        if (platform.system() == 'Darwin') | (platform.system() == 'Windows'):
            Device.pin_factory = MockFactory()

        # Get dimensions
        self.window.geometry('795x465')
        self.window.update()

        self.window.report_callback_exception = self.__handleException_callback__
        threading.excepthook = self.__handleException_callback__

        self.cont = False
        self.sock = None
        self.__sockTimeout__ = 9  # Allow 9s to connect to IP otherwise throw exception

    # Initialize the system
    def __call__(self):

        # Set the icon
        __p1__ = PhotoImage(file=os.path.join(super().__absPath__, 'pine_icon3.png'))
        self.window.iconphoto(False, __p1__)

        # Override default close option
        self.window.protocol('WM_DELETE_WINDOW', self.__initClose_callback__)

        # ####### CONSTRUCT TKINTER GUI
        self.frame1 = tk.Frame(self.window, bg=super().__frameBgColour__)
        self.frame1.grid(row=0, column=0, sticky='nsew')

        self.frame2 = tk.Frame(self.window, bg=super().__frameBgColour__)
        self.frame2.grid(row=0, column=1, sticky='nsew')

        self.window.grid_rowconfigure(0, minsize=790, weight=1)
        self.window.grid_columnconfigure(0, minsize=300)
        self.window.grid_columnconfigure(1, minsize=490)

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
        self.port.grid(row=2, column=0, padx=70, pady=(40, 5), sticky=W)

        # adding elements to frame2
        # MAIN LOGO
        super().__renderLogo__(self.frame2)

        # TEXT
        self.instr_text = Label(self.frame2, bg=super().__frameBgColour__,
                                text=f'Released on {self.releaseDate} \n'
                                     f'Developed by {self.dev}',
                                font=(super().__textFont__, super().__textFontSize__), fg=super().__colourSubHead__,
                                justify=LEFT)
        self.instr_text.pack(side=TOP, anchor='w')

        # Create message label
        self.labelMess = tk.Label(self.frame2, bg=super().__frameBgColour__,
                                  text='', font=(super().__textFont__, super().__HeadFontSize__),
                                  foreground=super().__colourText__)
        self.labelMess.pack(side=TOP, anchor='w', pady=50)

        # Add button frame
        self.buttonFrame = Frame(self.frame1, highlightthickness=0, borderwidth=0, background=super().__frameBgColour__)
        self.buttonFrame.grid(row=5, column=0, padx=70, pady=(40, 5), sticky=W)

        # Add RUN button
        self.runImage = super().__renderImageOnly__(50, 50, 'start_icon_grey.png')
        self.runImageFaded = super().__renderImageOnly__(50, 50, 'start_icon_faded.png')
        self.runButton = Button(self.buttonFrame, image=self.runImage, relief=FLAT,
                                compound=LEFT,  highlightthickness=0, borderwidth=0, highlightbackground='black',
                                command=self.__initSocket_callback__)
        self.runButton.pack(side=LEFT, padx=4)

        # Add STOP/RESET button
        self.stopImage = super().__renderImageOnly__(50, 50, 'stop_icon_grey.png')
        self.stopImageFaded = super().__renderImageOnly__(50, 50, 'stop_icon_faded.png')
        self.stopButton = Button(self.buttonFrame, image=self.stopImageFaded, compound=LEFT,  highlightthickness=0,
                                 borderwidth=0, highlightbackground='black', state=DISABLED, relief=FLAT,
                                 command=self.__initStop_callback__)
        self.stopButton.pack(side=LEFT, padx=4)

        # Add QUIT button
        self.quitImage = super().__renderImageOnly__(50, 50, 'quit_icon_grey.png')
        self.quitImageFaded = super().__renderImageOnly__(50, 50, 'quit_icon_faded.png')
        self.quitButton = Button(self.buttonFrame, image=self.quitImage, compound=LEFT,  highlightthickness=0,
                                 borderwidth=0, highlightbackground='black', command=self.__initQuit_callback__,
                                 relief=FLAT)
        self.quitButton.pack(side=LEFT, padx=4)

        # Load other images for later use
        self.yesImage = super().__renderImageOnly__(50, 50, 'yes_icon_grey.png')
        self.noImage = super().__renderImageOnly__(50, 50, 'no_icon_grey.png')

        # Set the broken pipe error check
        self.pipeCheck = tk.BooleanVar(False)
        self.pipeCheck.trace("w", self.__pipeBreakSafe__)

        # Set alternative socket error check
        self.unknownSockCheck = tk.BooleanVar(False)
        self.unknownSockCheck.trace("w", self.__sockBreakSafe__)

        # Set logic state, default IP and port values from text file
        self.__loadSetupFile__('setup.txt')

    # ####### CALLBACKS ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ###### ######
    # Handle uncaptured errors
    def __handleException_callback__(self, *_):
        """
        Globally handle any exceptions that have not been internally picked up (AFTER GUI is initialized).
        Check for out-of-memory error otherwise produces a general unknown error and logs the true error for debugging.
        """

        # Check if the memory is full due to too much usage
        if isinstance(sys.exc_info()[1], MemoryError):
            messagebox.showerror('Out of Memory Error',
                                 'Out of Memory. Please restart PiNe box and try again.')

        # ...otherwise log it and state that it is unknown
        else:
            messagebox.showerror('Unknown Error', 'Unknown error. Please check PiNe.log file for more information.')
        self.logger.error(traceback.format_exc())
        sys.exit()

    # Initiate socket connection on selecting Run callback
    def __initSocket_callback__(self):

        # Disable run button to avoid user initialising multiple threads
        self.runButton.config(state=DISABLED, image=self.runImageFaded)

        # Disable quit button to avoid forcing multi-thread shutdown
        self.quitButton.config(state=DISABLED, image=self.quitImageFaded)

        # Display status message
        self.labelMess.config(text='Establishing connection...', foreground=super().__colourText__)

        # Start countdown on separate first thread
        self.cont = True
        self.threadCountdown = threading.Thread(target=self.__countdown__, daemon=True)
        self.threadCountdown.start()

        # Initialize socket connection and check if successful (second thread)
        self.__host__ = self.varIP.get()
        self.__port__ = int(self.varPort.get())
        self.threadSock = threading.Thread(target=self.__initSocket__, daemon=True)
        self.threadSock.start()

    # Initiate stop sequence if system has started running
    def __initStop_callback__(self):

        # Close open socket (if established)
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.sock.close()
        self.sock = None

        # Close GPIO pins
        self.triggerSend.__closeGPIOs__()

        # Provide message
        self.labelMess.config(text='Connection stopped by user.', foreground=super().__colourText__)

        # Disable stop button
        self.stopButton.config(state=DISABLED, image=self.stopImageFaded)

        # Enable run button
        self.runButton.config(state=NORMAL, image=self.runImage)

        # Enable quit button
        self.quitButton.config(state=NORMAL, image=self.quitImage)

    # Query user quit window
    def __initQuit_callback__(self):

        # Open a TopLevel Window to check if user is sure
        self.quitWindow = Toplevel(self.window, bg=super().__frameBgColour__, bd=1, relief=RAISED)
        self.quitWindow.geometry('600x125')
        self.quitWindow.title('PiNe shutdown')

        # Create text label
        self.quitText = Label(self.quitWindow, bg=super().__frameBgColour__, text='Close application & shut down '
                                                                                  'PiNe box?',
                              fg=super().__colourText__, font=(super().__textFont__, super().__HeadFontSize__))
        self.quitText.pack(side=TOP, fill=BOTH, expand=TRUE)

        # Create buttons frame
        self.quitButtons = Frame(self.quitWindow, bg=super().__frameBgColour__)
        self.quitButtons.pack(side=TOP)

        # Add YES button to frame
        self.yesButton = Button(self.quitButtons, image=self.yesImage, relief=FLAT,
                                compound=LEFT, highlightthickness=0, borderwidth=0, highlightbackground='black',
                                command=self.__yesCallback__)
        self.yesButton.pack(side=LEFT, padx=4, pady=4)

        # Add NO button to frame
        self.noButton = Button(self.quitButtons, image=self.noImage, relief=FLAT,
                               compound=LEFT, highlightthickness=0, borderwidth=0, highlightbackground='black',
                               command=self.__noCallback__)
        self.noButton.pack(side=LEFT, padx=4, pady=5)

        # Center and 'freeze' the window in place
        super().__center__(self.quitWindow, 600, 125, 800, 480, 0, 0)
        super().__popupWindow__(self.quitWindow, freezeFlag=True)

    # Query user quit window
    def __initClose_callback__(self):

        # Open a TopLevel Window to check u
        self.closeWindow = Toplevel(self.window, bg=super().__frameBgColour__, bd=1, relief=RAISED)
        self.closeWindow.geometry('600x175')

        # Create text label
        self.closeText = Label(self.closeWindow, bg=super().__frameBgColour__, text='Close the PiNe application?',
                               fg=super().__colourText__, font=(super().__textFont__, super().__HeadFontSize__))
        self.closeText.pack(side=TOP, fill=BOTH, expand=TRUE)

        # Create second smaller text label with safe shut down warning message
        self.closeWarningText = Label(self.closeWindow, bg=super().__frameBgColour__, fg=super().__colourText__,
                                      font=(super().__textFont__, super().__textFontSize__), wraplength=580,
                                      text='WARNING: This will only close the application. '
                                           'Ensure that you still safely shut down the PiNe box OS before '
                                           'powering off at the switch.')
        self.closeWarningText.pack(side=TOP, fill=BOTH, expand=TRUE)

        # Create buttons frame
        self.closeButtons = Frame(self.closeWindow, bg=super().__frameBgColour__)
        self.closeButtons.pack(side=TOP)

        # Add YES button to frame
        self.yesCloseButton = Button(self.closeButtons, image=self.yesImage, relief=FLAT,
                                     compound=LEFT, highlightthickness=0, borderwidth=0, highlightbackground='black',
                                     command=self.__yesCloseCallback__)
        self.yesCloseButton.pack(side=LEFT, padx=4, pady=4)

        # Add NO button to frame
        self.noButton = Button(self.closeButtons, image=self.noImage, relief=FLAT,
                               compound=LEFT, highlightthickness=0, borderwidth=0, highlightbackground='black',
                               command=self.__noCloseCallback__)
        self.noButton.pack(side=LEFT, padx=4, pady=5)

        # Center and 'freeze' the window in place
        super().__center__(self.closeWindow, 600, 175, 800, 480, 0, 0)
        super().__popupWindow__(self.closeWindow, freezeFlag=True)

    # Callback when the quit button shutdown is confirmed by user
    def __yesCallback__(self, *_):
        self.__initShutDown_callback__()

    # Callback when the quit button shutdown is confirmed by user
    @staticmethod
    def __yesCloseCallback__(*_):
        sys.exit()

    # Callback when the quit button shutdown is cancelled by user
    def __noCallback__(self, *_):
        self.quitWindow.grab_release()
        self.quitWindow.destroy()

    # Callback when the quit button shutdown is cancelled by user
    def __noCloseCallback__(self, *_):
        self.closeWindow.grab_release()
        self.closeWindow.destroy()

    # Initiate quit/shutdown sequence
    @staticmethod
    def __initShutDown_callback__():

        if (platform.system() == 'Darwin') | (platform.system() == 'Windows'):
            sys.exit()  # Just close the Python program
        else:
            os.system('sudo shutdown -h now')   # Shut down Pi completely

    # ####### METHODS ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
    # Loads a setup file and sets various properties for the GUI to use and connect to socket
    def __loadSetupFile__(self, filename):

        # Try reading the setup file
        dirname = os.path.dirname(__file__)
        print(dirname)

        try:
            IPfile = open(dirname + '/' + filename, 'r')
        except Exception as inst:
            self.labelMess.config(text='Problem with setup.txt. Check log.', foreground=super().__colourText__)
            self.runButton.config(state=DISABLED, image=self.runImageFaded)

            # Log unknown error
            self.logger.exception(inst)
            return

        # Load LED duration value
        __LEDduration__ = str.rstrip(IPfile.readline())
        if (__LEDduration__[0:11] == 'LEDduration') & (__LEDduration__[12:] != ''):
            self.__LEDduration__ = float(__LEDduration__[12:])
        else:
            print([__LEDduration__[0:11], __LEDduration__[12:]])
            self.varIP.set('-')
            self.varPort.set('-')
            self.labelMess.config(text='Error with LEDduration in setup.txt', foreground=super().__colourText__)
            self.runButton.config(state=DISABLED, image=self.runImageFaded)
            return

        # Load default IP address
        __IPaddr__ = str.rstrip(IPfile.readline())
        if (__IPaddr__[0:2] == 'IP') & (__IPaddr__[3:] != ''):
            self.varIP.set(__IPaddr__[3:])
        else:
            self.varIP.set('-')
            self.varPort.set('-')
            self.labelMess.config(text='Error with IP address in setup.txt', foreground=super().__colourText__)
            self.runButton.config(state=DISABLED, image=self.runImageFaded)
            return

        # Load default IP address
        __port__ = str.rstrip(IPfile.readline())
        if (__port__[0:4] == 'PORT') & (__port__[5:] != ''):
            self.varPort.set(__port__[5:])
        else:
            self.varIP.set('-')
            self.varPort.set('-')
            self.labelMess.config(text='Error with PORT value in setup.txt', foreground=super().__colourText__)
            self.runButton.config(state=DISABLED, image=self.runImageFaded)
            return

    # Process to deal with closing safely when unexpected broken pipe occurs
    def __pipeBreakSafe__(self, *_):

        # Provide message
        self.labelMess.config(text='Connection lost. Check server connection.', foreground=super().__colourText__)

        # Disable stop button
        self.stopButton.config(state=DISABLED, image=self.stopImageFaded)

        # Enable run button
        self.runButton.config(state=NORMAL, image=self.runImage)

        # Enable quit button
        self.quitButton.config(state=NORMAL, image=self.quitImage)

    # Process to deal with closing safely when unexpected socket error occurs
    def __sockBreakSafe__(self, *_):

        # Provide message
        self.labelMess.config(text='Unknown sending error. Retry or check log.', foreground=super().__colourText__)

        # Disable stop button
        self.stopButton.config(state=DISABLED, image=self.stopImageFaded)

        # Enable run button
        self.runButton.config(state=NORMAL, image=self.runImage)

        # Enable quit button
        self.quitButton.config(state=NORMAL, image=self.quitImage)

    # Perform a countdown while establishing connection (until externally cancelled)
    def __countdown__(self):

        # Create countdown label
        self.countdownMess = tk.Label(self.frame2, bg=super().__frameBgColour__,
                                      text='', font=(super().__textFont__, super().__HeadFontSize__),
                                      foreground=super().__colourText__)
        self.countdownMess.pack(side=LEFT)

        stTime = self.__sockTimeout__
        t = stTime
        while (t > 0) & self.cont:
            self.countdownMess.config(text=str(t))
            time.sleep(1)
            t -= 1

    # Set up the initial socket connection with the server (threaded function)
    def __initSocket__(self):

        # Initialise socket and set up timeout limit for connecting
        if self.messType == 'UDP':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.settimeout(self.__sockTimeout__)

            try:

                # FOR UDP, PING CLIENT TO CHECK IF CONNECTED
                if platform.system() == 'Windows':
                    response = os.system("ping -n 1 " + self.__host__)
                else:
                    response = os.system("ping -c 1 " + self.__host__)

                # and then check the response...
                if response == 0:

                    # #### If connection successful, system then can only then be exited by stop button callback
                    # Stop countdown if still running
                    self.sock.connect((self.__host__, self.__port__))

                    # Send initial connection message
                    try:
                        initMess = 'c_PiNeConnected'
                        self.sock.sendall(PiNeRun.sendiXmess(initMess))

                    # Occurs if server is not listening at the specified port
                    except ConnectionRefusedError:

                        # Stop countdown and reset
                        self.cont = False
                        time.sleep(0.5)     # 'Hack' to ensure while loop in countdown is exited before changing label

                        # Destroy countdown and change label message text to unsuccessful
                        self.countdownMess.destroy()
                        self.labelMess.config(text='Connection refused while sending.', foreground=super().__colourText__)

                        # Disable stop button
                        self.stopButton.config(state=DISABLED, image=self.stopImageFaded)

                        # Enable run button
                        self.runButton.config(state=NORMAL, image=self.runImage)

                        # Enable quit button
                        self.quitButton.config(state=NORMAL, image=self.quitImage)

                        return

                    # Occurs if specific choice of IP or port is only permitted by sudo users
                    except PermissionError:

                        # Stop countdown and reset
                        self.cont = False
                        time.sleep(0.5)

                        # Destroy countdown and change label message text to unsuccessful
                        self.countdownMess.destroy()
                        self.labelMess.config(text='Permission denied while sending.', foreground=super().__colourText__)

                        # Disable stop button
                        self.stopButton.config(state=DISABLED, image=self.stopImageFaded)

                        # Enable run button
                        self.runButton.config(state=NORMAL, image=self.runImage)

                        # Enable quit button
                        self.quitButton.config(state=NORMAL, image=self.quitImage)

                        return

                    # #### If connection successful, system then can only then be exited by stop button callback
                    # Stop countdown if still running
                    self.cont = False
                    time.sleep(0.5)

                    # Overwrite text file with new correct values (after first trying to open), otherwise catch error
                    try:
                        # Try reading the setup file
                        dirname = os.path.dirname(__file__)

                        with open(dirname + '/' + 'setup.txt', 'w') as IPfile:
                            IPfile.write(f'LEDduration={self.__LEDduration__}\n'
                                         f'IP={self.varIP.get()}\nPORT={self.varPort.get()}')

                    except Exception as inst:
                        # Create 'success' message label
                        self.countdownMess.destroy()
                        self.labelMess.config(text='Problem with setup.txt. Check log.', foreground=super().__colourText__)

                        # Log unknown error
                        self.logger.exception(inst)

                        # Enable quit button
                        self.quitButton.config(state=NORMAL, image=self.quitImage)

                        return

                    # Instantiate PiNeRun instance and begin trigger listening (threaded)
                    self.triggerSend = PiNeRun(self.sock, self.pipeCheck, self.unknownSockCheck,
                                               logicState=self.__logicState__,
                                               LEDduration=self.__LEDduration__)
                    self.threadTrigg = threading.Thread(target=self.triggerSend, daemon=True)
                    self.threadTrigg.start()

                    # Create 'success' message label
                    self.countdownMess.destroy()
                    self.labelMess.config(text=' Connection successful.', foreground=super().__colourGood__)

                    # Enable stop button
                    self.stopButton.config(state=NORMAL, image=self.stopImage)

                    # Disable quit button
                    self.quitButton.config(state=DISABLED, image=self.quitImageFaded)

                else:
                    # Stop countdown and reset
                    self.cont = False
                    time.sleep(0.5)  # 'Hack' to ensure while loop in countdown is exited before destroying attributes

                    # Destroy countdown and change label message text to unsuccessful
                    self.countdownMess.destroy()
                    self.labelMess.config(text='PING to client failed.', foreground=super().__colourText__)

                    # Disable stop button
                    self.stopButton.config(state=DISABLED, image=self.stopImageFaded)

                    # Enable run button
                    self.runButton.config(state=NORMAL, image=self.runImage)

                    # Enable quit button
                    self.quitButton.config(state=NORMAL, image=self.quitImage)

                    return

            except Exception as inst:

                # Stop countdown and reset
                self.cont = False
                time.sleep(0.5)

                # Destroy countdown and change label message text to unsuccessful
                self.countdownMess.destroy()
                self.labelMess.config(text='Unknown connection error. Check log.', foreground=super().__colourText__)

                # Disable stop button
                self.stopButton.config(state=DISABLED, image=self.stopImageFaded)

                # Enable run button
                self.runButton.config(state=NORMAL, image=self.runImage)

                # Enable quit button
                self.quitButton.config(state=NORMAL, image=self.quitImage)

                # Log unknown error
                self.logger.exception(inst)

                return

        elif self.messType == 'TCP':
            self.sock = socket.socket()
            self.sock.settimeout(self.__sockTimeout__)

            try:
                self.sock.connect((self.__host__, self.__port__))

            # Occurs if a connection could not be established (often because IP or port is incorrect)
            except socket.timeout:

                # Stop countdown and reset
                self.cont = False
                time.sleep(0.5)       # 'Hack' to ensure while loop in countdown is exited before destroying attributes

                # Destroy countdown and change label message text to unsuccessful
                self.countdownMess.destroy()
                self.labelMess.config(text='Connection timed out.', foreground=super().__colourText__)

                # Disable stop button
                self.stopButton.config(state=DISABLED, image=self.stopImageFaded)

                # Enable run button
                self.runButton.config(state=NORMAL, image=self.runImage)

                # Enable quit button
                self.quitButton.config(state=NORMAL, image=self.quitImage)

                return

            # Occurs if server is not listening at the specified port
            except ConnectionRefusedError:

                # Stop countdown and reset
                self.cont = False
                time.sleep(0.5)

                # Destroy countdown and change label message text to unsuccessful
                self.countdownMess.destroy()
                self.labelMess.config(text='Connection refused.', foreground=super().__colourText__)

                # Disable stop button
                self.stopButton.config(state=DISABLED, image=self.stopImageFaded)

                # Enable run button
                self.runButton.config(state=NORMAL, image=self.runImage)

                # Enable quit button
                self.quitButton.config(state=NORMAL, image=self.quitImage)

                return

            # Occurs if specific choice of IP or port is only permitted by sudo users
            except PermissionError:

                # Stop countdown and reset
                self.cont = False
                time.sleep(0.5)

                # Destroy countdown and change label message text to unsuccessful
                self.countdownMess.destroy()
                self.labelMess.config(text='Permission denied.', foreground=super().__colourText__)

                # Disable stop button
                self.stopButton.config(state=DISABLED, image=self.stopImageFaded)

                # Enable run button
                self.runButton.config(state=NORMAL, image=self.runImage)

                # Enable quit button
                self.quitButton.config(state=NORMAL, image=self.quitImage)

                return

            # General exception for other errors (send general error message and log error for debugging)
            except Exception as inst:

                # Stop countdown and reset
                self.cont = False
                time.sleep(0.5)       # 'Hack' to ensure while loop in countdown is exited before destroying attributes

                # Destroy countdown and change label message text to unsuccessful
                self.countdownMess.destroy()
                self.labelMess.config(text='Unknown connection error. Check log.', foreground=super().__colourText__)

                # Disable stop button
                self.stopButton.config(state=DISABLED, image=self.stopImageFaded)

                # Enable run button
                self.runButton.config(state=NORMAL, image=self.runImage)

                # Enable quit button
                self.quitButton.config(state=NORMAL, image=self.quitImage)

                # Log unknown error
                self.logger.exception(inst)

                return

            # #### If connection successful, system then can only then be exited by stop button callback
            # Stop countdown if still running
            self.cont = False
            time.sleep(0.5)

            # Overwrite text file with new correct values (after first trying to open), otherwise catch error
            try:
                with open('setup.txt', 'w') as IPfile:
                    IPfile.write(f'LEDduration={self.__LEDduration__}\n'
                                 f'IP={self.varIP.get()}\nPORT={self.varPort.get()}')

            except Exception as inst:
                # Create 'success' message label
                self.countdownMess.destroy()
                self.labelMess.config(text='Problem with setup.txt. Check log.', foreground=super().__colourText__)

                # Log unknown error
                self.logger.exception(inst)

                # Enable quit button
                self.quitButton.config(state=NORMAL, image=self.quitImage)

                return

            # Create 'success' message label
            self.countdownMess.destroy()
            self.labelMess.config(text='Connection successful.', foreground=super().__colourGood__)

            # Send initial connection message
            initMess = 'c_PiNeConnected'
            self.sock.sendall(PiNeRun.sendiXmess(initMess))

            # Instantiate PiNeRun instance and begin trigger listening (threaded)
            self.triggerSend = PiNeRun(self.sock, self.pipeCheck, self.unknownSockCheck, logicState=self.__logicState__,
                                       LEDduration=self.__LEDduration__)
            self.threadTrigg = threading.Thread(target=self.triggerSend, daemon=True)
            self.threadTrigg.start()

            # Enable stop button
            self.stopButton.config(state=NORMAL, image=self.stopImage)

            # Disable quit button
            self.quitButton.config(state=DISABLED, image=self.quitImageFaded)


# Initialise and run tkinter loop
def main(ver, releaseDate, dev):

    if getattr(sys, 'frozen', False):
        __absPath__ = str(Path.home())
    else:
        __absPath__ = os.path.dirname(os.path.abspath(__file__))

    LOG_FILENAME = os.path.join(Path.home(), 'Desktop/PiNe.log')
    PINElogger = logging.getLogger()
    PINElogger.setLevel(logging.ERROR)
    PINEformatter = logging.Formatter('%(asctime)s;%(levelname)s;%(message)s')
    PINEhandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=int(5e6), backupCount=3)  # 5MB size limit
    PINEhandler.setFormatter(PINEformatter)
    PINElogger.addHandler(PINEhandler)

    # Initialise the GUI
    try:
        app = PiNeMain(ver, releaseDate, dev, PINElogger)
        app()
    except Exception as inst:
        messagebox.showerror('Unknown startup error', 'Unknown startup error. Please check PiNe.log file for '
                                                      'more information.')
        PINElogger.exception(inst)
        sys.exit()

    app.window.mainloop()


# #### MAIN to run application ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
if __name__ == '__main__':
    main()
