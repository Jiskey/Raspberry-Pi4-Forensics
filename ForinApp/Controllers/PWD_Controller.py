#Python FSI_Controller (File System Inspection)
#Application Name: Forin
#Author: J.Male
#Desc: 
#	Handles all of the operations within the application realting to File System Inspection And The Sleuth Kit.

import click
import sys
import os

from View import MainMenu_Controller
from Model.PwdObject import PwdObject
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms
from Scripts import UsageLoggingScript as uls

"""

"""
def PWD_main_menu(path = '0'):
	choices = []
	title = ''

	if path and path != '0':
		evi_path = path
		if evi_path.endswith('/') == False:
			evi_path = evi_path + '/'
	else:
		evi_path = scs.settings_check('$Default_Output_Location')
		if evi_path.endswith('/') == False:
			evi_path = evi_path + '/'

	os.system('clear')
	click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')
	click.echo('Hashcat is a powerful hash cracking tool with many options to assist in this demanding task')
	click.echo('Password Cracking Is A very Demanding Task! Expect System Slowdown')	

	click.echo('\nCurrent Image Evidance Location: {}\n'.format(evi_path))

	title = 'Please Select A File That Contains The Hash Lines To Crack:'
	for file in os.listdir(evi_path):
		if os.path.isfile(evi_path + str(file)) == True and str(file).startswith('.') == False:
			choices.append(file)
	choices.append('[1] -- Specify Hash File Evidance Directory')
	choices.append('[0] Back')
	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		MainMenu_Controller.main_menu()
	elif index_selection == len(choices) - 2:
		index_selection = tms.generate_string_menu('Hash File Evidance Directory:', 1)
		if index_selection == '0':
			PWD_main_menu()
		else:
			PWD_main_menu(index_selection)
	else:
		pwd_object = PwdObject(evi_path, choices[index_selection])

	PWD_hash_type(pwd_object)

"""
"""
def PWD_hash_type(pwd_object):
	choices = ['MD5', 'SHA1', 'SHA2-256', 'SHA2-512', 'NTLM' ,'[1] Select From List', '[0] back']
	title = 'Please Select The hash Type Of The Has You wish To Crack'	

	os.system('clear')
	click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')
	click.echo('Below Are Some Common Hashes, Can View Hashcat List with Option [1]')

	index_selection = tms.generate_menu(title, choices)

	if index_selection == 6:
		PWD_main_menu(pwd_object.get_filepath())
	elif index_selection == 5:
		PWD_main_menu(pwd_object.get_filepath())
	else:
		PWD_main_menu(pwd_object.get_filepath())