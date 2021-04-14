"""
Classes to define all the elements in the main window interface

Kirubin Pillay, Maria Cobo 30.12.2020
"""


from tkinter import *
from GUIaes import GUIaes
# from tkinter.ttk import *


# #### CLASS for initializing and navigating the app ############################################


 # Initiate run buttons
 #        self.__initRunBar__()


    # def __initRunBar__(self):
    #     # self.runBarWindow = Frame(self.PiNeMain.frame2, bg='white')
    #     # self.runBarWindow.pack(padx=self.tabpadx, fill='both')
    #
    # # Add CLEAR button
    #     self.clearButton = Button(self.frame2, text=' Clear all',
    #                           bg='white', fg='black', font=(super().__textFont__, super().__HeadFontSize__),
    #                           padx=5, pady=5, state=DISABLED) #add command command=self.__clearEntries__
    #     self.clearButton.pack(side=LEFT, fill='both', padx=2)
    #
    # # Add RUN button
    #     self.runImage = super().__renderImageOnly__(self.helpImage_h / 1.2, self.helpImage_h / 1.4, 'runImage_1.png')
    #     self.runImage_fade = super().__renderImageOnly__(self.helpImage_h / 1.2, self.helpImage_h / 1.4,
    #                                                  'runImage_1_faded.png')
    #     self.runButton = Button(self.runBarWindow, text=' Calculate API', image=self.runImage_fade, compound=LEFT,
    #                         bg='white', fg='black', font=(super().__textFont__, super().__HeadFontSize__),
    #                         padx=5, pady=5, command=self.__runAPI_callback__, state=DISABLED)
    #     self.runButton.pack(side=LEFT, fill='both', padx=2)
    #

# class GUIentry(Frame):
#     def __init__(self, parent):
#         super().__init__(parent)
#         s = Style()
#         s.configure('Pink.TEntry', background='hot pink')


def validate(P):
    test = re.compile('(^\d{0,3}$|^\d{1,3}\.\d{0,3}$|^\d{1,3}\.\d{1,3}\.\d{0,3}$|^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{0,3}$)')
    if test.match(P):
        return True
    else:
        return False
