#Python Settings_Controller
#Desc: Handles operations relating to the settings of the program

import click
import sys
import os

from Scripts import ErrorScript as es
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms

from Controllers import MainMenu_Controller

from Classes.Setting import Setting

def settings_main():
	global saved_changes			

	#settings = scs.get_settings_txt()			#get settings (returns a list of file lines)
	settings_list = scs.get_settings_list()			#Returns a List of settings classes (filled with correct txt file lines)
	os.system('clear')

	click.secho('Program Settings\n', fg='blue', bold=True)
	
	try:
		print(len(saved_changes))
		if len(saved_changes) > 0:
			click.secho('Changes Made To Settings! You Will Be Promted On exit!\n', bold=True, fg='red')
			for count, change in enumerate(saved_changes):
				change_code = change.get_code()
				change_call, change_var = change_code.split(':')
				print('Change Made To: {}   From: {}   To:{}'.format(change_call, scs.settings_check(change_call), change_var))
				#code, old, new = change.split('/')
				#click.echo('Changes Made To: {}   Changed: {} -> {}'.format(code, old, new))
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

	if index_selection == len(choices) - 1:
		try:
			if len(saved_changes) > 0:
				settings_save_menu(settings_list)
			else:
				MainMenu_Controller.main_menu()
		except:
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

def settings_edit_menu(setting):
	click.echo('\n' + setting.get_description())
	setting_code = setting.get_code()
	call, var = setting_code.split(':')

	click.echo('Currently Saved Option: ' + scs.settings_check(call))

	choices = []
	items = setting.get_items()[1:-1]
	items = items.split('][')
	for count, item in enumerate(items):
		choices.append(item)
	choices.append('[0] Cancel')
	title = '\nPlease Select An Option:'

	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		settings_main()
	else:	
		new_code = call + ':' + choices[index_selection]

		try:
			dupe_found = False
			print('LETS GO')
			for count, change in enumerate(saved_changes):
				change_code = change.get_code()
				change_call, change_var = change_code.split(':')
				if call == change_call:
					print('DUPE_FOUND')
					dupe_found = True
					change.set_code(new_code)

			if dupe_found != True:
				print('LETS GO')
				setting.set_code(new_code)
				saved_changes.append(setting)
				
		except:
			print('OIOIOIOIOI')
			setting.set_code(new_code)
			saved_changes.append(setting)

		#x=input('-')

		settings_main()

def settings_save_menu(settings_list):
	choices = ['[1] Save','[2] Discard', '[0] Back']
	title = '\nChanges Have Been Made, Would You Like To Save The New Config?'

	index_selection = tms.generate_menu(title, choices)

	if index_selection == 0:
		new_settings = []
		settings_txt = scs.get_settings_txt()			#get settings (returns a list of file lines)

		for count, change in enumerate(saved_changes):
			change_code = change.get_code()
			change_call, change_var = change_code.split(':')
			setting_index = scs.settings_index(change_call)
			settings_txt[setting_index] = (change_code + '\n')

		scs.settings_update(settings_txt)
		MainMenu_Controller.main_menu()

	elif index_selection == 2:
		settings_main()
	elif index_selection == 1:
		MainMenu_Controller.main_menu()
