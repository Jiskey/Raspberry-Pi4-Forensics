#Python Main Menu Controller
#Application Name: Forin
#Author: J.Male
#Desc: 
#	First Menu The User See's In The Application (Main Menu)
#	Sends The User To Multiple Different Controllers Based On Their Input

import click
import sys
import os

from Controllers import ACQ_Controller
from Controllers import DC_Controller
from Controllers import PDF_Controller
from Controllers import FSI_Controller
from Controllers import PWD_Controller
from Controllers import Settings_Controller
from Controllers import Extras_Controller
from Scripts import TerminalMenuScript as tms

"""
Acts As The Main Menu For The Program And Is Called To Return To The Start
"""
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
	click.echo('-  Version: 1.0.0 23/04/2021')
	click.echo('-  Kali Version: 2021.1')
	click.echo('-  Desc: "FORIN" is a simple CLI app that allows you to perform quick/easy digital anylsis and')
	click.echo('         investigation using the tools included with Kali Linux')
	click.echo('\n-  More Information: https://github.com/Jiskey/Raspberry-PI4-Forensics')
	click.echo('\n######################################################################################################')
	click.echo('\nIMPORTANT NOTE: BE SURE TO RUN AS SU!')
	click.echo('IMPORTANT NOTE: Kali v2021.1 Does Not Include Dc3dd, Dcfldd & Foremost By Default')

	sub_menu_1()

"""
Acts As The Selection First Menu For The Program
"""
def sub_menu_1():
	choices = ["[1] Tools", "[2] Extras", '[3] Settings', "[0] Exit"]
	title = '\nWelcome! What would You Like To Do?'

	selection_index = tms.generate_menu(title, choices)
	if selection_index == 0:
		sub_menu_2()
	elif selection_index == 1:
		Extras_Controller.extras_main()
	elif selection_index == 2:
		Settings_Controller.settings_main()
	elif selection_index == 3:
		sys.exit(0)
	else:
		sys.exit(0)

"""
Acts As a Sub Menu For Tools
Allows The User To Select A Type Of Forensic Discipline
"""
def sub_menu_2():
	choices = ['[1] Acquire Img (Dc3dd / Dcfldd)', 
			'[2] File System Inspection (Sleuth Kit)',
			'[3] Data Carving (Foremost / Scalpel / PhotoRec)',
			'[4] PDF File Analysis (Pdfid / Pdf-Parser)',
			'[5] Password Cracking (Hashcat)', 
			'[0] Back']
	title = '\nPlease Select A Tool You Would Like To You!'
	selection_index = tms.generate_menu(title, choices)

	if selection_index == 0:
		ACQ_Controller.ACQ_selection()
	if selection_index == 1:
		FSI_Controller.FSI_main_menu()
	elif selection_index == 2:
		DC_Controller.DC_main_menu()
	elif selection_index == 3:
		PDF_Controller.PDF_main_menu()
	elif selection_index == 4:
		PWD_Controller.PWD_main_menu()
	elif selection_index == 5:
		sub_menu_1()
	else:
		sys.exit(0)
