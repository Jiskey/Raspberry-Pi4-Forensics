#Python DC_Controller (Data Carving)
#Desc: Handles all of the operations within the application realting to Data Carving

import click
import sys
import os

from Controllers import MainMenu_Controller

from Scripts import ErrorScript as es
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms

def DC_selection():
	os.system('clear')

	click.secho('2.1: Data Carving', fg='blue', bold=True)

	click.echo('\nData Carving Using Scalpel')
	click.echo('\nCurrent Output Path: {}'.format(scs.settings_check('$DC_Output_Location')))

	title = '\nWhat Would You Like To Carve?'
	choices = ['[1] Connected Drive','[2] Acquired Img File','[0] Back']
	index_selection = tms.generate_menu(title, choices)

	choices = []	
	if index_selection == 0:
		pass
	elif index_selection == 1:
		title = '\nWhat Would You Like To Carve?\nIf You Dont See Any Files Try Specifying a Custom Path'
		path = scs.settings_check('$Default_Output_Location')
		for file in os.listdir(path):
			if file.lower().endswith('.dd') or file.lower().endswith('.img') or file.lower().endswith('.raw') or file.lower().endswith('.aff'):
				choices.append(file)
		choices.append('-- Specify Other Output Location')
		choices.append('[0] Back')
	elif index_selection == 2:
		MainMenu_Controller.main_menu()

	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		DC_selection()
	elif index_selection == len(choices) - 2:
		path = tms.generate_string_menu('Directory', 1)
	else:
		MainMenu_Controller.main_menu()
