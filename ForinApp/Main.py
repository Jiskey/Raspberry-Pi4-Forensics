# FORIN - KALI LINUX DIGITAL FORENSIC INVESTIGATOR
# By: J. Male
# Version: 0.0.2 30/01/2021
# DESC: Forin is a simple CLI app that allows you to perform quick/easy digital anylsis and
#	investigation using the tools included with Kali Linux.
# More Information: https://github.com/Jiskey/Raspberry-PI4-Forensics

import sys
import click
from simple_term_menu import TerminalMenu

from Controllers import GUI_Controller
from Controllers import ACQ_Controller

def main():
	terminal_menu = TerminalMenu(['Entry1','Entry2','Entry3', 'bg_blue'])
	menu_entry_index = terminal_menu.show()

if __name__ == '__main__':
	main()	
	selection = GUI_Controller.main_menu(0)
	

#Acquisition
	if selection == 'ACQ':
		ACQ_Controller.ACQ_selection()










