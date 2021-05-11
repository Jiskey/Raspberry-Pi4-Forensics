#Python Settings_Controller
#Application Name: Forin
#Author: J.Male
#Desc: 
#	Handles operations relating to the settings of the program
#	uses a Settings Class To Handle changes To the Config/Settings.txt file

import click
import sys
import os
import time

from View import MainMenu_Controller
from Model.Setting import Setting
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms
from Scripts import UsageLoggingScript as uls

"""
main settings call. acts as the first page in the settings menu.
has global var 'saved_changes' to store changes made
"""
def settings_main():
	global saved_changes					#global var to detect any changes made			

	settings_list = scs.get_settings_list()	
	os.system('clear')
	click.secho('Program Settings\n', fg='blue', bold=True)
	
	### check for any saved changes and display
	try:
		if len(saved_changes) > 0:
			click.secho('Changes Made To Settings! You Will Be Promted On exit!\n', bold=True, fg='red')
			for count, change in enumerate(saved_changes):
				change_code = change.get_code()
				change_call, change_var = change_code.split(':')
				print('Change Made To: {}   From: {}   To:{}'.format(change_call, scs.settings_check(change_call), change_var))
		else:
			click.secho('No Changes Made To Settings', bold=True, fg='green')
	except:
		click.secho('No Changes Made To Settings', bold=True, fg='green')
		saved_changes = []

	tmp = ''
	choices = []
	for count, setting in enumerate(settings_list):
		if tmp != setting.get_section():
			tmp = setting.get_section()
			choices.append(setting.get_section().strip())
	choices.append('[0] Save & Exit')
	title = '\nProgram & Tool Settings:'
	
	index_selection = tms.generate_menu(title, choices)

	### go to save menu if changes made or gather setting for menu
	if index_selection == len(choices) - 1:
		if len(saved_changes) > 0:
			settings_save_menu(settings_list, saved_changes)
		else:
			MainMenu_Controller.main_menu()
	else:																																											
		choices2 = []
		for count, setting in enumerate(settings_list):
			if setting.get_section() == choices[index_selection]:
				title = '\n' +  setting.get_section()
				tmp = setting.get_code()
				tmp = tmp.split(':')
				choices2.append(tmp[0][1:])
		choices2.append('[0] Back')
	
	index_selection = tms.generate_menu(title, choices2)

	if index_selection == len(choices2) - 1:
		settings_main()
	else:
		for count, setting in enumerate(settings_list):
			tmp = setting.get_code()
			tmp = tmp.split(':')
			if choices2[index_selection] == tmp[0][1:]:
				settings_edit_menu(setting)

"""
settings edit menu for editing a setting
using string formating to change and edit sections
requires a setting which is of setting.class
"""
def settings_edit_menu(setting):
	#split setting code to get the setting and its state
	try:
		click.echo('\n' + setting.get_description())
		setting_code = setting.get_code()
		call, var = setting_code.split(':')
	except:
		click.echo('Fatal Error In Config/Settings.txt File. Cannot Edit Setting. Please Check For Corruption')
		time.sleep(3)
		settings_main()

	click.echo('Currently Saved Option: ' + scs.settings_check(call))

	choices = []
	items = setting.get_items()[1:-1]
	items = items.split('][')
	for count, item in enumerate(items):
		choices.append(item)
	choices.append('[0] Cancel')
	title = '\nPlease Select An Option:'

	index_selection = tms.generate_menu(title, choices)

	### If menu requires string input instead of set selections
	new_code = call + ':' + choices[index_selection]
	if choices[index_selection].find('--') != -1:
		if choices[index_selection].find('Directory') != -1:
			string_selection = tms.generate_string_menu('Image Name', 1)
		else:
			string_selection = tms.generate_string_menu('Image Name', 0)	
		if string_selection == '0':
			settings_main()
		else:
			new_code = call + ':' + string_selection.strip()

	if index_selection == len(choices) - 1:
		settings_main()
	### Update Settings List
	else:	
		try:
			dupe_found = False
			for count, change in enumerate(saved_changes):			
				change_code = change.get_code()
				change_call, change_var = change_code.split(':')
				if call == change_call:					
					dupe_found = True
					change.set_code(new_code)			

			if dupe_found != True:
				setting.set_code(new_code)		
				saved_changes.append(setting)
				
		except:
			setting.set_code(new_code)
			saved_changes.append(setting)

		settings_main()

"""
settings save menu called on exit if there are changes made
requires a setting_list which is a list of setting.classes
"""
def settings_save_menu(settings_list, changes):
	choices = ['[1] Save','[2] Discard', '[0] Back']
	title = '\nChanges Have Been Made, Would You Like To Save The New Config?'

	index_selection = tms.generate_menu(title, choices)

	### get settings (returns a list of file lines) and Update Settings.txt
	if index_selection == 0:
		settings_txt = scs.get_settings_txt()

		for count, change in enumerate(changes):
			change_code = change.get_code()
			change_call, change_var = change_code.split(':')
			setting_index = scs.settings_index(change_call)
			settings_txt[setting_index] = (change_code + '\n')

		logfile = scs.settings_check('$Default_UsageLog_Location')
		if logfile.endswith('/') == False:
			logfile += '/'
		logfile += 'Settings_Usage_Logs.txt'
		uls.log_change(logfile, 'Settings_Change', changes)

		scs.settings_update(settings_txt)
		saved_changes = []
		MainMenu_Controller.main_menu()

	elif index_selection == 2:
		settings_main()
	elif index_selection == 1:
		saved_chages = []
		MainMenu_Controller.main_menu()
