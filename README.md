# PiNEbox
The following README.md describes the procedure for developing and installing the PiNe Box including the user interface.
The PiNe box is an enclosed device run with a Raspberry Pi that allows for the simultaneous triggering of events and time stamping between an EEG system as well as an external Vital Signs monitor. The system reads in TTL triggers from external triggering devices that are simultaneously sent to an EEG amplifier and sends a UDP message to the Vital Signs monitor via an ethernet network link. A GUI allows the user to seledt the appropriate IP address and listening ports. 

These instructions are for six input triggers (Push Button, Lance, Tactile, Auditory, Visual and Experimental/Pin Prick stimuli) using TTL specification and the vital signs system is currently assumed to be iXTrend developed by iXcellence: https://www.ixellence.com/index.php/en/home/17-default-en/products

Authors/Developers: Kirubin Pillay, Maria Cobo Andrade, Alan Worley, Caroline Hartley 08/06/2021
Paediatric Neuroimaging Group, University of Oxford, Oxford, UK.
Great Ormond Street Hospital, London, UK.

## Current Version
Version 1.0 (Released 07/06/2021)

## Citation
A manuscript is currently in development and will require citing once published. The citation will be provided here.

## Readme structure
To develop the PiNe box, this repository contains the following information:
1. Instructions for building the PiNe box and setting up the Raspberry Pi. Go to the folder 'PiNeBox_setup' which contains two files:
a. 'PiNeBox_hardware' - Instructions for constructing the PiNe box hardware including parts lists, key datasheets and circuit diagrams.
b. 'PiNeBox_software' - Instructions for setting up the Raspberry Pi OS (this guide assumes Raspbian is installed on the Pi).

## Downloading and Installing the Git Repository
### Dependencies
This code requires Python 3.7.0 or higher.

### On a PC/Mac (for developers)
1. To install the repository on a PC/Mac for editing/further development:

```
git clone https://github.com/kpillay/PiNEbox.git
cd PiNEbox. 
pip install -r requirements.txt
```

2. Run `cli.py` to begin PiNe UI.

### On a Raspberry Pi (for non-developers)
1. The Pi typically comes installed with Python 2 and possibly a version of Python 3 (<3.7.0) at least on the Raspbian OS. If this is the case, Python 3.7 will first need to be installed and symlinked to the `python` command when run on the terminal. To achieve this, follow the instructions found in: https://installvirtual.com/install-python-3-7-on-raspberry-pi/. Otherwise skip to step 3.

2. After following the instructions in Step 1, the pip installer will likely still be pointing to a previous python instance. To avoid this clash, download and install the repository with the following commands (assuming python 3.7 is now symlinked by `python` in the terminal. Note this will download a read-only version of the repository and is recommended when simply wanting to deploy the current software version on your Pi for non-developer use.

```
git clone git://github.com/kpillay/PiNEbox.git
cd PiNEbox
python -m pip install -r requirements.txt
```

3. To run the PiNe UI, run `cli.py` directly in the terminal using the following command:
```
python cli.py
```
