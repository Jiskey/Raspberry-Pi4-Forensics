#Python Settings_Controller
#Desc: Handles operations relating to the settings of the program

import click
import sys
import os

from Scripts import ErrorScript as es
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms

from Controllers import MainMenu_Controller

def settings_main():
	global saved_changes			
	global settings

	saved_changes = []
	settings = scs.get_settings()			#get settings (returns a list of file lines)

	os.system('clear')

	click.secho('Program Settings', fg='blue', bold=True)

	choice_count = 0
	choices = []
	for count, line in enumerate(settings):		#Get Main Headers as Choices.
		if line.find('-----') != -1:
			choice_count = choice_count + 1
			a = line.split('-----')
			choices.append('[' + str(choice_count) + '] ' + a[1].strip())
	choices.append('[0] Back')
	title = '\nProgram & Tool Settings:'
	
	settings_dict = {			#child choice dictonary
		'Sect':[],
		'Desc':[],
		'Items':[],
		'Code':[]
	}
	store_sets = False
	line_count = 0

	index_selection = tms.generate_menu(title, choices)
	
	for count, line in enumerate(settings):
			if store_sets == True:
				if line.find('$') != -1:
					settings_dict['Code'].append(line[:-1])
				elif line.find('---') != -1:
					settings_dict['Sect'].append(line)
				elif line.find('#') != -1:
					settings_dict['Desc'].append(line[:-1])
				elif line.find('[') != -1:
					settings_dict['Items'].append(line[:-1])
				elif line.find('-----') != -1:
					store_sets = False
					#settings_dict['Sect'].append(line)
					#print(settings_dict['Desc'][count])
					#print(settings_dict['Items'][count])
					#print(settings_dict['Code'][count])
					#print(settings[scs.settings_index('Default_Tool')])
					break	
			elif line.find('-----') != -1:
				if line_count == index_selection:
					store_sets = True
				else:
					line_count = line_count + 1

	if index_selection == len(choices) - 1:
		MainMenu_Controller.main_menu()
	else:
		settings_child_menu(settings_dict)


def settings_child_menu(settings_dict):
	for count, change in enumerate(saved_changes):
		click.echo(saved_changes[count])

	choices = []
	for count, choice in enumerate(settings_dict['Code']):
		selection = choice
		dol, selection = selection.split('$')
		setting, var = selection.split(':')
		choices.append(setting)
	choices.append('[0] Save & Exit')
	title = ''

	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		Settings_main()
	else:
		settings_edit_menu(index_selection, settings_dict)


def settings_edit_menu(settings_code, settings_dict):
		#print(desc + items + code)
		os.system('clear')
		click.secho('Program Settings', fg='blue', bold=True)
		
		setting, var = settings_dict['Code'][settings_code].split(':')		

		a = settings_dict['Items'][settings_code][1:-1]
		choices = a.split('][')
		choices.append('[0] Cancel')
		title = '\nPlease Select An Option:'

		index_selection = tms.generate_menu(title, choices)

		if index_selection == len(choices) - 1:
			settings_child_menu(settings_dict)
		else:
			updated_var = choices[index_selection]
			updated_setting = setting + ':' + updated_var + '\n' 
			settings[scs.settings_index(setting)] = updated_setting
			settings_dict['Code'][settings_code] = updated_setting
			saved_changes.append('Changes Made To: {} - {} -> {}'.format(setting, var, updated_var))
			settings_child_menu(settings_dict)
		
"""
	x = True
	while x == True:
		index_selection = tms.generate_menu(title, choices)
		for count, line in enumerate(settings):
			if store_sets == True:
				if line.find('$') != -1:
					child_choices.append(line[:-1])
				elif line.find('-----') != -1:
					store_sets = False
					print(child_choices)
					print(settings[scs.settings_index('Default_Tool')])
					break	
			elif line.find('-----') != -1:
				if line_count == index_selection:
					store_sets = True
				else:
					line_count = line_count + 1
		if child_choices.count('$') != 0:
			print('YES')
		else:
			es.error(3000, 0)

	
	#for count, line in enumerate(settings):
	#	if line[:2].find('$') != -1:
	#		print(line)
	#print(scs.settings_index('$Default_Tool'))
"""
