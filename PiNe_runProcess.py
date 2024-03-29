"""
This is the backend run procedure for the PiNe box project.
A call to this class is performed in a parallel thread on selecting the 'Run' button on the main GUI.

Class PiNErun performs general UDP messaging between PiNe box client and iXTrend server.
Assumes a socket connection is already established and passes in the socket object.

Kirubin Pillay 19/05/2020
"""

import platform
import socket
import time
from gpiozero import LED, Button
from signal import pause


# #### CLASS to initialise the generak trigger sending procedure ###### ###### ###### ###### ###### ###### ######
class PiNeRun:

    # Init. variables
    def __init__(self, sock, pipeCheck, unknownSockCheck, logicState='HIGH', LEDduration=0.5):

        # Set input variables to properties
        self.sock = sock
        self.pipeCheck = pipeCheck
        self.unknownSockCheck = unknownSockCheck
        self.logicState = True if logicState == 'HIGH' else False    # 'HIGH' is negative logic, 'LOW' is postive logic
        self.LEDduration = LEDduration

        # Set GPIO pins to appropriate LEDs (output states)
        self.ledButton = LED(23)            # Push-button
        self.ledPinPrick = LED(22)          # PinPrick
        self.ledVisual = LED(21)            # Visual
        self.ledAudio = LED(27)             # Audio
        self.ledLance = LED(12)             # Lance
        self.ledForce = LED(20)             # Force

        # Set read-in GPIO pins to check for triggers (uses Button module)
        self.inputButton = Button(16, pull_up=self.logicState)       # Push-button
        self.inputPinPrick = Button(19, pull_up=self.logicState)                      # PinPrick
        self.inputVisual = Button(25, pull_up=self.logicState)                        # Visual
        self.inputAudio = Button(24, pull_up=self.logicState)                         # Audio
        self.inputLance = Button(18, pull_up=self.logicState)                         # Lance
        self.inputForce = Button(17, pull_up=self.logicState)                         # Force

    # Run the main trigger send/receive from the PiNe box
    def __call__(self):

        self.inputButton.when_pressed = self.act_PushButton
        self.inputPinPrick.when_pressed = self.act_PinPrick
        self.inputVisual.when_pressed = self.act_Visual
        self.inputAudio.when_pressed = self.act_Audio
        self.inputLance.when_pressed = self.act_Lance
        self.inputForce.when_pressed = self.act_Force

        pause()

    # ####### CALLBACKS ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
    # Callback to perform push button activation protocol
    def act_PushButton(self):
        try:
            tic = time.perf_counter()

            MESS = 'PushButton'
            self.sock.sendall(self.sendiXmess(MESS))    # Send the message to server

            # Flash the LEDs
            self.ledButton.on()
            time.sleep(self.LEDduration)
            self.ledButton.off()

        except BrokenPipeError:
            self.pipeCheck_protocol()

        except Exception as inst:
            self.logger.exception(inst)
            self.unknownSocket_protocol()

    # Callback to perform PinPrick activation protocol
    def act_PinPrick(self):
        try:
            MESS = 'PinPrick'
            self.sock.sendall(self.sendiXmess(MESS))    # Send the message to server

            # Flash the LEDs
            self.ledPinPrick.on()
            time.sleep(self.LEDduration)
            self.ledPinPrick.off()

        except BrokenPipeError:
            self.pipeCheck_protocol()

        except Exception as inst:
            self.logger.exception(inst)
            self.unknownSocket_protocol()

    # Callback to perform Visual activation protocol
    def act_Visual(self):
        try:
            MESS = 'Visual'
            self.sock.sendall(self.sendiXmess(MESS))    # Send the message to server

            # Flash the LEDs
            self.ledVisual.on()
            time.sleep(self.LEDduration)
            self.ledVisual.off()

        except BrokenPipeError:
            self.pipeCheck_protocol()

        except Exception as inst:
            self.logger.exception(inst)
            self.unknownSocket_protocol()

    # Callback to perform Audio activation protocol
    def act_Audio(self):
        try:
            MESS = 'Auditory'
            self.sock.sendall(self.sendiXmess(MESS))    # Send the message to server

            # Flash the LEDs
            self.ledAudio.on()
            time.sleep(self.LEDduration)
            self.ledAudio.off()

        except BrokenPipeError:
            self.pipeCheck_protocol()

        except Exception as inst:
            self.logger.exception(inst)
            self.unknownSocket_protocol()

    # Callback to perform Lance activation protocol
    def act_Lance(self):
        try:
            MESS = 'Heellance'
            self.sock.sendall(self.sendiXmess(MESS))    # Send the message to server

            # Flash the LEDs
            self.ledLance.on()
            time.sleep(self.LEDduration)
            self.ledLance.off()

        except BrokenPipeError:
            self.pipeCheck_protocol()

        except Exception as inst:
            self.logger.exception(inst)
            self.unknownSocket_protocol()

    # ####### METHODS ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### ####### #######
    # Callback to perform Force activation protocol
    def act_Force(self):
        try:
            MESS = 'Tactile'
            self.sock.sendall(self.sendiXmess(MESS))    # Send the message to server

            # Flash the LEDs
            self.ledForce.on()
            time.sleep(self.LEDduration)
            self.ledForce.off()

        except BrokenPipeError:
            self.pipeCheck_protocol()

        except Exception as inst:
            self.logger.exception(inst)
            self.unknownSocket_protocol()

    # Perform standardized setup to escape due to broken pipe
    def pipeCheck_protocol(self):

        # Close open socket (if established)
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.sock.close()
        self.sock = None

        # Close GPIO pins
        self.__closeGPIOs__()

        # Triggers callback in PiNE_master to safely handle broken pipe errors
        self.pipeCheck.set(True)

    # Perform standardized setup to escape due to an unknown error
    def unknownSocket_protocol(self):

        # Close open socket (if established)
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.sock.close()
        self.sock = None

        # Close GPIO pins
        self.__closeGPIOs__()

        # Triggers callback in PiNE_master to safely handle these errors
        self.unknownSockCheck.set(True)

    # Close GPIOs explicitly if program closes unexpectedly
    def __closeGPIOs__(self):

        # Close GPIO pins to appropriate LEDs
        if hasattr(self, 'ledButton'):
            self.ledButton.close()        # Push-button
        if hasattr(self, 'ledPinPrick'):
            self.ledPinPrick.close()      # PinPrick
        if hasattr(self, 'ledVisual'):
            self.ledVisual.close()        # Visual
        if hasattr(self, 'ledAudio'):
            self.ledAudio.close()         # Audio
        if hasattr(self, 'ledLance'):
            self.ledLance.close()         # Lance
        if hasattr(self, 'ledForce'):
            self.ledForce.close()         # Force

        # Close read-in GPIO pins to check for triggers
        if hasattr(self, 'inputButton'):
            self.inputButton.close()       # Push-button
        if hasattr(self, 'inputPinPrick'):
            self.inputPinPrick.close()     # PinPrick
        if hasattr(self, 'inputVisual'):
            self.inputVisual.close()       # Visual
        if hasattr(self, 'inputAudio'):
            self.inputAudio.close()        # Audio
        if hasattr(self, 'inputLance'):
            self.inputLance.close()        # Lance
        if hasattr(self, 'inputForce'):
            self.inputForce.close()        # Force

    # Send an iXTrend-formatted UDP message
    @staticmethod
    def sendiXmess(MESSAGE):

        # Compile UDP message
        start = bytes([0 for i in range(0, 8)])
        end = bytes([0 for i in range(0, 8)])
        message_len = bytes([len(MESSAGE)])
        my_str_as_bytes = str.encode(MESSAGE)
        iX_message = start + end + message_len + my_str_as_bytes

        return iX_message

        toc = time.perf_counter()

        print(f"Time for code to run was {toc - tic :0.2f}seconds")

