"""
General class containing specific GUI aesthetics variables to be inherited by the main GUI call

Kirubin Pillay, Maria Cobo 30.12.2020

"""
from tkinter import *
from PIL import ImageTk
import PIL.Image
from tkinter import messagebox, Canvas, TOP
import os
import platform
import sys
from pathlib import Path


# #### CLASS containing general GUI properties and methods to be inherited by other classes ############################
class GUIaes:
    # Formatting variables
    __textFont__ = 'Open Sans'
    __titleFontSize__ = 30
    __HeadFontSize__ = 24
    __subHeadFontSize__ = 14
    __helpFontSize__ = 12
    __textFontSize__ = 12
    __frameBgColour__ = '#504f51'
    __colourSubHead__ = '#808080'
    __colourText__ = '#f28e7c'
    __colourGood__ = '#61b299'

    if getattr(sys, 'frozen', False):
        __absPath__ = str(Path.home())
    else:
        __absPath__ = os.path.dirname(os.path.abspath(__file__))

    __imageLogo__ = PIL.Image.open(os.path.join(__absPath__, 'PiNeBox_logo.png'))

    # Render a general image for buttons etc.
    def __renderImageOnly__(self, width, height, ImageName):
        image = PIL.Image.open(os.path.join(self.__absPath__, ImageName))
        image.thumbnail((int(width), int(height)), PIL.Image.ANTIALIAS)
        photoImage = ImageTk.PhotoImage(image)

        return photoImage

    # Render the logo
    def __renderLogo__(self, master):
        self.canvas_for_image = Canvas(master, height=int(180), width=int(420), borderwidth=0, highlightthickness=0,
                                       bg='#504f51')
        self.imageResized = ImageTk.PhotoImage(self.__imageLogo__.resize((int(420), int(180)), PIL.Image.ANTIALIAS))

        self.imageOnCanvas = self.canvas_for_image.create_image(0, 0, image=self.imageResized, anchor='nw')
        self.canvas_for_image.itemconfig(self.imageOnCanvas, image=self.imageResized)
        self.canvas_for_image.pack(anchor='nw', pady=(50, 1))
