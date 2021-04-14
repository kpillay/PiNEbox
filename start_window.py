"""
Main GUI for the PiNE box project
v BETA: interface and functions to add automatic triggers to the vital signs recordings

Kirubin Pillay, Maria Cobo 30/12/2020
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


# #### CLASS to initialise the main PiNe GUI ###############################################
class PiNeMain(GUIaes):

    def __init__(self, ver, releaseDate, dev):

        self.ver = ver
        self.releaseDate = releaseDate
        self.dev = dev

        self.window = tk.Tk()
        self.window.geometry('800x480')
        self.window.resizable(0, 0)
        self.window.title(f'PiNe - version {self.ver}')

        # Set the icon
        __p1__ = PhotoImage(file=os.path.join(super().__absPath__, 'pine_icon3.png'))
        self.window.iconphoto(False, __p1__)

# #### adding frames to the window  #####

        self.frame1 = tk.Frame(self.window, bg=super().__frameBgColour__)
        self.frame1.grid(row=0, column=0, sticky='nsew')

        self.frame2 = tk.Frame(self.window, bg=super().__frameBgColour__)
        self.frame2.grid(row=0, column=1, sticky='nsew')

        self.window.grid_rowconfigure(0, minsize=480, weight=1)
        self.window.grid_columnconfigure(0, minsize=300) # weight=1 # minsize=100
        self.window.grid_columnconfigure(1, minsize=500) # weight=1 # minsize=100,

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
        varIP = tk.StringVar()
        vcmd = self.frame1.register(validate)
        self.ipadd = tk.Entry(self.frame1, textvariable=varIP, width=14,
                              highlightthickness=0, highlightcolor=super().__frameBgColour__, bg=super().__colourText__,
                              highlightbackground=super().__frameBgColour__, borderwidth=0,
                              font=(super().__textFont__, super().__HeadFontSize__), fg=super().__frameBgColour__,
                              validate='key', validatecommand=(vcmd, '%P'))
        self.ipadd.grid(row=0, column=0, padx=70, pady=(100, 5))

        # port entry
        varPort = tk.StringVar()
        self.port = tk.Entry(self.frame1, textvariable=varPort, width=8, highlightthickness=0,
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

        # Add RUN button
        self.runImage = super().__renderImageOnly__(50, 50, 'start_icon.png')
        # self.runImage_fade = super().__renderImageOnly__(self.helpImage_h / 1.2, self.helpImage_h / 1.4, 'runImage_1_faded.png')
        self.runButton = Button(self.frame2,image=self.runImage,
                                compound=LEFT,  highlightthickness=0, borderwidth=0, highlightbackground='black') # command=self.__runAPI_callback__, state=DISABLED)
        self.runButton.pack(side=LEFT, padx=2)


# Initialise and run tkinter loop
def main(ver, releaseDate, dev):

    if getattr(sys, 'frozen', False):
        __absPath__ = str(Path.home())
    else:
        __absPath__ = os.path.dirname(os.path.abspath(__file__))


    # Run the GUI
    # try:
        app = PiNeMain(ver, releaseDate, dev)
    # except Exception as inst:
    #     messagebox.showerror('UNKNOWN ERROR', 'UNKNOWN ERROR: Please contact system administrator')
    #     sys.exit()

    app.window.mainloop()


# #### MAIN to run application ########################################################################################
if __name__ == '__main__':
    main()