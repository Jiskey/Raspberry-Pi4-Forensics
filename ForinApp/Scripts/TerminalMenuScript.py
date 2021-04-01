#Python Terminal_Menu Script
#using simple_term_menu 

import click
import sys
import os
import time

from simple_term_menu import TerminalMenu

from Scripts import SettingsCheckScript as scs
"""
genernate_menu creates a selection menu
takes (string, list of items)
"""
def generate_menu(menu_title, menu_items):
	menu = TerminalMenu(
		menu_entries = menu_items,
		title = menu_title,
		menu_cursor = scs.settings_check('$Cursor_Style'),
		menu_cursor_style = ('fg_' + scs.settings_check('$Cursor_Colour'), "bold"),
		menu_highlight_style = ('bg_' + scs.settings_check('$Highlight_Colour'), 'fg_' + scs.settings_check('$Text_Colour')),
		cycle_cursor = True,
		exit_on_shortcut = False,
		#clear_screen = True,
	)

	selection_index = menu.show()
	return selection_index

"""
generate_file_preview_menu creats a menu to display files within a given directory
takes in a title and a filepath
"""
def generate_file_preview_menu(menu_title, filepath):
	def files(path = filepath):
		return (file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)))

	menu = TerminalMenu(
		menu_entries = files(),
		title = menu_title,
		menu_cursor = scs.settings_check('$Cursor_Style'),
		menu_cursor_style = ('fg_' + scs.settings_check('$Cursor_Colour'), "bold"),
		menu_highlight_style = ('bg_' + scs.settings_check('$Highlight_Colour'), 'fg_' + scs.settings_check('$Text_Colour')),
		cycle_cursor = True,
		exit_on_shortcut = False,
		#clear_screen = True,
		preview_command = 'cat ' + filepath + '{}',
		preview_size = 0.7,
	)

	selection_index = menu.show()
	return selection_index

"""
Generates a Normal string input selection screen (simple_term_menu support problem)
takes in a title and returns a string
Performs a check (num) if one is required
"""
def generate_string_menu(title, num):
	click.echo('\nPlease Specify A Custom {}:'.format(title))
	click.echo('Back/Cancel = "0", "exit", "quit", "cancel", "back"')
	
	check = 0
	x = True
	while x == True:
		string_selection = input('\n--> ')
		cancel_opts = ["0", "exit", "quit", "cancel", "back"]
	
		for count, opts in enumerate(cancel_opts):
			if string_selection == opts:
				string_selection = '0'
				return string_selection
		
		if num == 1:
			if os.path.isdir(string_selection) == True:
				return string_selection
			elif os.path.isdir(string_selection) == False and check == 0:
				check = check + 1
				print('Invalid Selection, Please Specify A Valid Selection')
			else:
				pass
		elif num == 0:
			return string_selection

"""
Gererates a Menu with 2 selections
takes in a title and a sleep time
uses time module to specify sleep time to prevent 'Enter Spam'
"""
def generate_promt_menu(title, freeze):
	menu_items = ['CANCEL', 'EXECUTE']

	menu = TerminalMenu(
		menu_entries = menu_items,
		title = title,
		menu_cursor = scs.settings_check('$Cursor_Style'),
		menu_cursor_style = ('fg_' + scs.settings_check('$Cursor_Colour'), "bold"),
		menu_highlight_style = ('bg_' + scs.settings_check('$Highlight_Colour'), 'fg_' + scs.settings_check('$Text_Colour')),
		cycle_cursor = True,
		exit_on_shortcut = False,
		#clear_screen = True,
	)

	time.sleep(freeze)
	selection_index = menu.show()
	return selection_index



