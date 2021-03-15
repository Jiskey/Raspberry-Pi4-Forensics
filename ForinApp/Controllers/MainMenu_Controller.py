#GUI_Controller
#Desc: Handles Execution Of GUI elements within the application.

import click
import sys
import os

from Controllers import ACQ_Controller

from Scripts import TerminalMenuScript as tms

#Generate Application Header
def main_menu():
	os.system('clear')

	click.echo('\n######################################################################################################')
	click.secho('    ___ ___  ___             _      ___ _  _            _   _           _           ', bold=True)
	click.secho('   | __/ _ \| _ \___ _ _  __(_)__  |_ _| \| |_ _____ __| |_(_)__ _ __ _| |_ ___ _ _ ', bold=True)
	click.secho('   | _| (_) |   / -_) ` \(_-< / _|  | || .` \ V / -_|_-<  _| / _` / _` |  _/ _ \ `_|', bold=True)
	click.secho('   |_| \___/|_|_\___|_||_/__/_\__| |___|_|\_|\_/\___/__/\__|_\__, \__,_|\__\___/_|  ', bold=True)
	click.secho('                                                             |___/                  ', bold=True) 
	click.secho('\n-  FORIN - KALI LINUX DIGITAL FORENSIC INVESTIGATOR', bold=True, fg='blue')
	click.echo('-  By: J. Male')
	click.echo('-  Version 0.0.3: 13/03/2021')
	click.echo('-  Kali Version: 2020.4')
	click.echo('-  Desc: "FORIN" is a simple CLI app that allows you to perform quick/easy digital anylsis and')
	click.echo('         investigation using the tools included with Kali Linux')
	click.echo('\n-  More Information: https://github.com/Jiskey/Raspberry-PI4-Forensics')
	click.echo('\n######################################################################################################')
	click.echo('\nIMPORTANT NOTE: BE SURE TO RUN AS SU!')

	#Generate Main Menu Options
	choices = ["[1] Aquire A New Image", "[2] Analyse Exsisting Image", "[3] Settings", "[0] Exit"]
	title = '\nWelcome! What would You Like To Do?'

	#Detect User Selection
	x = False
	while x == False:
		selection_index = tms.generate_menu(title, choices)
		if selection_index == 0:
			ACQ_Controller.ACQ_selection()
			x = True
			break
		elif selection_index == 1:
			sys.exit(0)
			x = True
			break
		elif selection_index == 2:
			sys.exit(0)
			x = True
			break
		elif selection_index == 3:
			sys.exit(0)
			x = True
			break
	return code









