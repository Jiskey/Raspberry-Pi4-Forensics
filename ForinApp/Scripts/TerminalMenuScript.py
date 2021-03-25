#Python Terminal_Menu Script
#using simple_term_menu 

import click
import sys
import os

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
		menu_highlight_style = ('bg_' + scs.settings_check('$Highlight_Colour'), 'fg_' + scs.settings_check('$Text_Highlight_Colour')),
		cycle_cursor = True,
		exit_on_shortcut = False,
		#clear_screen =True,
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
		menu_highlight_style = ('bg_' + scs.settings_check('$Highlight_Colour'), 'fg_' + scs.settings_check('$Text_Highlight_Colour')),
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
	print('\nPlease Specify A Custom {}:'.format(title))
	print('Back/Cancel = "0", "exit", "quit", "cancel", "back"')

	string_selection = input('\n--> ')

	cancel_opts = ["0", "exit", "quit", "cancel", "back"]
	
	for count, opts in enumerate(cancel_opts):
		if string_selection == opts:
			string_selection = '0'
			return string_selection

	if num == 1:
		print()
	else:
		return string_selection







