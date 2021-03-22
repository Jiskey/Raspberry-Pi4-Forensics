#Python Terminal_Menu Script
#using simple_term_menu 

from simple_term_menu import TerminalMenu

from Scripts import SettingsCheckScript as scs
"""
genernate_menu creates a selection menu
takes (string, list of items)
"""
def generate_menu(title, items):
	menu_title = title
	menu_items = items

	menu = TerminalMenu(
		menu_entries = menu_items,
		title = menu_title,
		menu_cursor = scs.settings_check('$Cursor_Style'),
		menu_cursor_style = ('fg_' + scs.settings_check('$Cursor_Colour'), "bold"),
		menu_highlight_style = ('bg_' + scs.settings_check('$Highlight_Colour'), 'fg_' + scs.settings_check('$Text_Highlight_Colour')),
		cycle_cursor = True,
		#show_shortcut_hints = True,
		exit_on_shortcut = False,
		#clear_screen =True,
	)

	selection_index = menu.show()
	return selection_index
