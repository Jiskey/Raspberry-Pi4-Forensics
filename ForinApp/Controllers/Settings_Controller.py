#Python Settings_Controller
#Desc: Handles operations relating to the settings of the program

import click
import sys
import os

from Scripts import ErrorScript as es
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms

def Settings_main():
	os.system('clear')

	click.secho('Program Settings', fg='blue', bold=True)

	settings = scs.get_settings()			#get settings

	choice_count = 0
	choices = []
	for count, line in enumerate(settings):		#Get Main Headers as Choices.
		if line.find('-----') != -1:
			choice_count = choice_count + 1
			a = line.split('-----')
			choices.append('[' + str(choice_count) + '] ' + a[1].strip())
	choices.append('[0] Back')
	title = '\n.'
	
	child_choices = []
	store_sets = False
	line_count = 0

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
