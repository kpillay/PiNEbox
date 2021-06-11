# PiNEbox
The following README.md describes the procedure for developing and installing the PiNe Box including the user interface.
The PiNe box is an enclosed device run with a Raspberry Pi that allows for the simultaneous triggering of events and time stamping between an EEG system as well as an external Vital Signs monitor. The system runs a Python UI that reads in TTL triggers from external triggering devices (that are simultaneously sent to an EEG amplifier) and sends a UDP message to the Vital Signs monitor via an ethernet network link. A GUI allows the user to select the appropriate IP address and listening ports. 

These instructions are for six input triggers (Push Button, Lance, Tactile, Auditory, Visual and Experimental/Pin Prick stimuli) using TTL specification and the vital signs system is currently assumed to be iXTrend developed by iXcellence: https://www.ixellence.com/index.php/en/home/17-default-en/products

Authors/Developers: Kirubin Pillay, Maria Cobo Andrade, Caroline Hartley, Alan Worley 07/06/2021
Paediatric Neuroimaging Group, University of Oxford, Oxford, UK.
Great Ormond Street Hospital, London, UK.

## Current Version
Version 1.0 (Released 07/06/2021)

## Citation
A manuscript is currently in development and will require citing once published. The citation will be provided here.

## Repository Structure
To develop the PiNe box, this repository contains the following information:
1. **PiNe Box construction instructions:** Building the PiNe box and setting up the Raspberry Pi Including datasheets, schematics etc. Go to the folder 'PiNeBox_setup' in the repository. Begin with the pdf 'PiNeBox_hardware' for overall instructions for constructing the PiNe box.
2. **Raspberry Pi OS software configuration**: Instructions for setting up the Raspberry Pi OS (this guide assumes a recent version of Raspbian is already installed on the Pi) - see rest of this readme documentation.
3. **The Python UI**: Source code to develop and run the Python UI on the configured Raspberry Pi. See rest of this readme for instructions on how to run and automatically start on boot.

## Downloading the Git Repository
### Dependencies
The OS software instructions assumes a recent version of Raspbian Jessie is already installed on the Pi.
The Python UI code requires Python 3.7.0 or higher.

### On a PC/Mac (for developers)
1. To download and install the repository on a PC/Mac for editing/further development:

```
git clone https://github.com/kpillay/PiNEbox.git
cd PiNEbox. 
pip install -r requirements.txt
```

### On a Raspberry Pi (for non-developers)
1. The Pi typically comes installed with Python 2 and possibly a version of Python 3 (<3.7.0) at least on the Raspbian OS. If this is the case, Python 3.7 will first need to be installed and symlinked to the `python` command when run on the terminal. To achieve this, follow the instructions found in: https://installvirtual.com/install-python-3-7-on-raspberry-pi/. If already set up, skip to step 3.

2. After following the instructions in Step 1, the pip installer will likely still be pointing to a previous python instance. To avoid this clash, download and install the repository with the following commands (assuming python 3.7 is now symlinked by `python` in the terminal. Note this will download a read-only version of the repository and is recommended when simply wanting to deploy the current software version on your Pi for non-developer use.

```
git clone git://github.com/kpillay/PiNEbox.git
cd PiNEbox
python -m pip install -r requirements.txt
```

## Configuring the Raspberry Pi software for PiNe box use
A few adaptations to the software must by made in order for it to best work with the PiNe box hardware and the Python UI. This includes installing a vietual keyboard for use on the touch screen.

### Initial updating of software
Before proceeding, update the Raspbian OS to the latest version. To do this enter the following commands into the Pi terminal (ensure an internet connection is first established on the Pi via WiFi or ethernet):
```
sudo apt-get update
sudo apt-get upgrade
sudo shutdown -r now
```
After the Pi has updated and shut down. Reboot and proceed as below below.

### Enabling the activity LED
The soft shutdown button utilizes the TxD pin on the Pi GPIO to provide the user with an indicator of the current CPU state. This pin needs to be enabled in the software to power the LED. To do this:
1. On the Pi, open up the file `\boot\config.txt`
2. At the end of the file, add the line `enable_uart=1`, then save and close.
3. Reboot the pi and the activity LED should now turn on.

### Installing a virtual keyboard for the touch screen
The matchbox-keyboard is chosen here. To install it and create a shortcut on the toolbar:
1. Install keyboard by typing in the Pi Terminal `sudo apt-get install matchbox-keyboard`.
2. Reboot the pi
3. The keyboard can now be found in Menu -> Accessories-> Keyboard. To create a taskbar shortcut, right click taskbar then select Add/Remove Panel Items. Add the ‘Application Launch Bar’.
4. Right click the taskbar again, select 'Application Launch and Taskbar', navigate to 'Keyboard' under 'Accessories' and click 'Add'.
5. The keyboard shortcut should now be on the taskbar at the top of the screen.

### Aesthetic changes (optional)
#### Changing the Raspbian OS colour scheme
To create a more professional, bespoke look to your Pi's OS in preparation for running the Python UI, you can alter the colours.
The taskbar and window background and colours can be changed to match the Python UI by navigating to the Pi start menu, selecting 'Preferences' and opening the 'Appearance' settings. The following HEX colour codes can be used:
 - Background colour changes to match Python UI scheme: #504f51
 - Text colour changes: #f28e7c

#### Changing the wallpaper
A PiNe Box wallpaper is also included in the respository and called 'PiNe_wallpaper.png'. This can also be added in the above settings.


## Running the PiNe Box UI

### On Terminal
To run the PiNe UI on PC/Mac/Raspberry Pi, simply run `cli.py` in your chosen IDE. To run directly in the terminal, cd to the repository location and use the following command:
```
python cli.py
```

### Testing the Python UI
The Python UI can be tested by setting the IP address to localhost (127.0.0.1) and running the script as above. Opening a parallel python session with the provided server scripts PiNe_macServerUDP.py and PiNe_macServerTCP.py based on the messaging choice will allow testing that the cli.py scripts are successfully sending messages back to your local machine.

### Setting up to automatically run when Pi boots up
Once the Python UI can be successfully opened as above using the terminal, it can be set up to automatically open whenever the Pi boots. **The following instructions assumes the PiNEbox repository folder is on the desktop**:
1. Open up the autostart script in the Pi terminal by typing `sudo nano /etc/xdg/lxsession/LXDE-pi/autostart`.
2. At the bottom of the file, add the following command to run a preconfigured bash script: `/home/pi/Desktop/PiNEbox/PiNe_startup.sh`.
3. The preconfigured bash script 'PiNe_startup' will run the Python UI code.
4. Reboot the pi and the Python UI should now open automatically.

