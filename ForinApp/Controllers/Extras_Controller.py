#Extras_Controller
#Desc: Handles Execution Of the Extras section in the application.

import click
import sys
import os

from View import MainMenu_Controller
from Scripts import TerminalMenuScript as tms
from Scripts import SettingsCheckScript as scs
from Scripts import FdiskScript as fds

"""
main function extras_main, displays selection of extra's
"""
def extras_main():
	os.system('clear')
	click.secho('2. Program Extras\n', fg='blue', bold=True)

	choices = ['[1] View Img/Usability Logs', '[2] Enable/Disable SSH', '[3] Fdisk Drive Search', '[0] Back']
	title = 'Please Select An Extra'
	
	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		MainMenu_Controller.main_menu()
	elif index_selection == 0:
		extras_logs(scs.settings_check('$Default_Hash_Logging_Location'))
	elif index_selection == 1:
		extras_ssh()
	elif index_selection == 2:
		extras_drives()

"""
extras_logs, searches a directory for files and display its contents.
requires a path where files will located
preview is a combination of TMS & cat
"""
def extras_logs(log_path):
	choices = []
	if os.path.isdir(log_path) == False:
		es.error(4000, 0)
	elif os.path.isdir(log_path) == True:
		choices.append('[1] Acqusition Logs')
		choices.append('[2] Usabiltiy Logs')
	choices.append('[0] Back')
	title = 'Using Path: {}\n'.format(log_path)

	index_selection = tms.generate_menu(title, choices)
	
	if log_path.endswith('/') == False:
		log_path+= '/'

	title = title + '\n--- Press "Enter" To Return\n'
	check = 0
	if index_selection == 0:
		index_selection = tms.generate_file_preview_menu(title, log_path, 'all')
	elif index_selection == 1:
		index_selection = tms.generate_file_preview_menu(title, scs.settings_check('$Default_UsageLog_Location'), 'all')
	elif index_selection == len(choices) -1:
		extras_main()

	extras_logs(log_path)

"""
performs the 'fdisk' command and displays its full output (verbose)
"""
def extras_drives():
	click.echo('Device Information Found Using Command: fdisk -l')
	click.echo('Currently Display Full List Of Returns Given By Fdisk\n')

	connected_drives = fds.fdisk(True)

	x = input('--- Press "Enter" To Return')
	extras_main()

"""
extras_ssh, menu controller to allow the enabling/disabling of SHH
CURRENTLY NOT IS USE!!!
"""
def extras_ssh():
	extras_main()	
