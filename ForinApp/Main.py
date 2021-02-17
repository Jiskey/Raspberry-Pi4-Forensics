# FORIN - KALI LINUX DIGITAL FORENSIC INVESTIGATOR
# By: J. Male
# Version: 0.0.2 30/01/2021
# DESC: Forin is a simple CLI app that allows you to perform quick/easy digital anylsis and
#	investigation using the tools included with Kali Linux.
# More Information: https://github.com/Jiskey/Raspberry-PI4-Forensics

import sys
import click

from Controllers import GUI_Controller
from Controllers import ACQ_Controller

if __name__ == '__main__':
	selection = GUI_Controller.main_menu(0)

#Acquisition
	if selection == 'ACQ':
		ACQ_Controller.ACQ_selection()










