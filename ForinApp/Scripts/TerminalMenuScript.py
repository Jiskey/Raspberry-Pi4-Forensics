#Python simple_term_menu Script
#Application Name: Forin
#Author: J.Male
#Desc: 
#	Using Simple_term_menu to generate multiple differing types of input menus.
#	Contains File Preview, Multi selection, standard Selection, prompt, string (default) Menus

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
	)

	selection_index = menu.show()
	return selection_index

"""
generate_obj_preview_menu generates a file preview menu based on the name of the current select obj.
uses 'cat' command to generate small preview window
"""
def generate_obj_preview_menu(menu_title, menu_items, objs_list, dir_path):
	menu = TerminalMenu(
		menu_entries = menu_items,
		title = menu_title,
		menu_cursor = scs.settings_check('$Cursor_Style'),
		menu_cursor_style = ('fg_' + scs.settings_check('$Cursor_Colour'), "bold"),
		menu_highlight_style = ('bg_' + scs.settings_check('$Highlight_Colour'), 'fg_' + scs.settings_check('$Text_Colour')),
		cycle_cursor = True,
		exit_on_shortcut = False,
		preview_command = 'cat ' + dir_path + '{}.txt',
		preview_size = 0.8,
	)

	selection_index = menu.show()
	return selection_index

"""
generate_file_preview_menu creats a menu to display files within a given directory
takes in a title and a filepath
"""
def generate_file_preview_menu(menu_title, dir_path):
	def files(path = dir_path):
		return (file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file != 'README.txt')

	menu = TerminalMenu(
		menu_entries = files(),
		title = menu_title,
		menu_cursor = scs.settings_check('$Cursor_Style'),
		menu_cursor_style = ('fg_' + scs.settings_check('$Cursor_Colour'), "bold"),
		menu_highlight_style = ('bg_' + scs.settings_check('$Highlight_Colour'), 'fg_' + scs.settings_check('$Text_Colour')),
		cycle_cursor = True,
		exit_on_shortcut = False,
		preview_command = 'cat ' + dir_path + '{}',
		preview_size = 0.6,
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
		
		if num == 1 and string_selection != '':
			if os.path.isdir(string_selection) == True:
				return string_selection
			elif os.path.isdir(string_selection) == False and check == 0:
				check = check + 1
				print('Invalid Selection, Please Specify A Valid Selection')
			else:
				pass
		elif num == 0 and string_selection != '':
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
		menu_highlight_style = ('bg_' + scs.settings_check('$Highlight_Colour'), 'fg_' + scs.settings_check('$Text_Colour')),
		cycle_cursor = True,
		exit_on_shortcut = False,
	)

	time.sleep(freeze)
	selection_index = menu.show()
	return selection_index

"""
Gererates a Menu with Multiple selection func
takes in a title, a list of choices and a type check
uses type_check to return either a tuple(indices(0, 1, 4. etc) or tuple(str, str, str, etc...))
"""
def gernerate_multi_select_menu(title, choices, type_check):
	menu_items = choices

	menu = TerminalMenu(
		menu_entries = menu_items,
		title = title,
		menu_cursor = scs.settings_check('$Cursor_Style'),
		menu_cursor_style = ('fg_' + scs.settings_check('$Cursor_Colour'), "bold"),
		menu_highlight_style = ('bg_' + scs.settings_check('$Highlight_Colour'), 'fg_' + scs.settings_check('$Text_Colour')),
		cycle_cursor = True,
		exit_on_shortcut = False,
		multi_select = True,
		show_multi_select_hint=True
	)

	index_selection_indices = menu.show()
	if type_check == False:
		return index_selection_indices
	elif type_check == True:
		return menu.chosen_menu_entries


