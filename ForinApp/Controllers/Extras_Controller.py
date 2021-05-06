#Python Extras Controller
#Application Name: Forin
#Author: J.Male
#Desc: 
#	Handles Execution Of the Extras Section In The Application.
#	An Extra Is Usually An Additonal internal System rather Then a Tool (Exceptions).

import click
import sys
import os

from View import MainMenu_Controller
from Scripts import TerminalMenuScript as tms
from Scripts import SettingsCheckScript as scs
from Scripts import FdiskScript as fds

"""
Main Function, Displays Selection of Extra's To The User
"""
def extras_main():
	os.system('clear')
	click.secho('2. Program Extras\n', fg='blue', bold=True)

	choices = ['[1] View Img/Usability Logs', '[2] Fdisk Drive Search','[3] View Cracked Hashes (Hashcat)', '[4] Check Hashes In a Directory (MD5)', '[0] Back']
	title = 'Please Select An Extra'
	
	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		MainMenu_Controller.main_menu()
	elif index_selection == 0:
		extras_logs(scs.settings_check('$Default_Hash_Logging_Location'))
	elif index_selection == 1:
		extras_drives()
	elif index_selection == 2:
		extras_cracked_hashes(scs.settings_check('$Default_PWD_Output'))
	elif index_selection == 3:
		extras_hash_comp()

"""
Extras_Logs, Searches a Directory For Files And Display Its Contents.
Requires A Path Where Files Will Be Located
Preview Is a combination of simple_term_menu & cat
"""
def extras_logs(log_path):
	choices = []
	if os.path.isdir(log_path) == True:
		choices.append('[1] Acqusition Logs')
		choices.append('[2] Usabiltiy Logs')
	choices.append('[0] Back')
	title = 'Using Path: {}\n'.format(log_path)

	index_selection = tms.generate_menu(title, choices)
	
	if log_path.endswith('/') == False:
		log_path+= '/'

	title = title + '\n--- Press "Enter" To Return\n'
	if index_selection == 0:
		index_selection = tms.generate_file_preview_menu(title, log_path)
	elif index_selection == 1:
		index_selection = tms.generate_file_preview_menu(title, scs.settings_check('$Default_UsageLog_Location'))
	elif index_selection == len(choices) -1:
		extras_main()

	extras_logs(log_path)

"""
Performs the 'fdisk' command and displays its full output (Verbose) Incl. Ram (If Appl.)
"""
def extras_drives():
	click.echo('Device Information Found Using Command: fdisk -l')
	click.echo('Currently Display Full List Of Returns Given By Fdisk\n')
	connected_drives = fds.fdisk(True)
	wait_selection = tms.generate_menu('Please Press Any Button To Continue', [' '])
	extras_main()

"""
Displays A List Of Cracked Password Found In the Hashcat potfile.
Will Also Display FileFound in PWD Evidance Folder.
"""
def extras_cracked_hashes(log_path):
	if log_path.endswith('/') == False:
		log_path+= '/'

	click.secho('Hashes Cracked From ~/root/Hashcat.potfile: ', bold=True)
	click.echo('Checking File...\n')
	os.system('sudo cat ~/.hashcat/hashcat.potfile')
	click.echo('\nCurrently selected Craches Hashes Output File: {}\n'.format(log_path))

	title ='\n--- Press "Enter" To Return\n'
	index_selection = tms.generate_file_preview_menu(title, log_path)

	extras_main()

"""
Lets the user specify a directory and display the MD5 hashes of each file
uses Md5deep the check MD5 hashes
"""
def extras_hash_comp():
	click.echo('Using Md5deep To Perfrom Hashing Of Files')
	index_selection = tms.generate_string_menu('Path The Check The MD5 hash Of Each File: ', 1)
	if index_selection == '0':
		extras_main()
	else:
		os.system('sudo md5deep -r {}'.format(index_selection))
		wait_selection = tms.generate_menu('\nPlease Press Any Button To Continue', [' '])
		extras_hash_comp()
	
	