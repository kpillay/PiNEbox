"""
General class containing specific GUI aesthetics variables to be inherited by the main GUI call

Maria Cobo, Kirubin Pillay 30.12.2020

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
    __HeadFontSize__ = 18
    __labelFontSize__ = 12
    __textFontSize__ = 10
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
        self.canvas_for_image = Canvas(master, height=int(170), width=int(350), borderwidth=0, highlightthickness=0,
                                       bg='#504f51')
        self.imageResized = ImageTk.PhotoImage(self.__imageLogo__.resize((int(350), int(170)), PIL.Image.ANTIALIAS))

        self.imageOnCanvas = self.canvas_for_image.create_image(0, 0, image=self.imageResized, anchor='nw')
        self.canvas_for_image.itemconfig(self.imageOnCanvas, image=self.imageResized)
        self.canvas_for_image.pack(anchor='nw', pady=(50, 1))

    # Center the specified popup window
    @staticmethod
    def __center__(master, w, h, ws, hs, xrel, yrel):
        """
        Center a tkinter Toplevel window based on relative screen and GUI dimensions.

        :param tkinter.Toplevel master: Tkinter Toplevel window to centralize
        :param int w: Width of Toplevel window
        :param int h: Height of Toplevel window
        :param int ws: Width of screen
        :param int hs: Height of screen
        :param int xrel: Relative horizontal shift of GUI relative to user's screen(s)
        :param int yrel: Relative vertical shift of GUI relative to user's screen(s)
        :return: None
        """

        x = xrel + (ws // 2) - (w // 2)
        y = yrel + (hs // 2) - (h // 2)
        master.geometry('+%d+%d' % (x, y))

    # Common settings to embed any popup window
    @staticmethod
    def __popupWindow__(master, freezeFlag=True):
        """
        Method to change popup window settings and priorities (e.g. freeze background, shift window focus etc.)

        :param tkinter.Toplevel master: Tkinter Toplevel window
        :param bool freezeFlag: If True, will additionally keep this Toplevel window on top of other windows
            and freeze their functionality until user addresses the Toplevel window.
        :return: None
        """

        master.overrideredirect(1)
        master.overrideredirect(0)
        if freezeFlag:
            master.grab_set()
            master.attributes('-topmost', 'true')
