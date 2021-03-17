from simple_term_menu import TerminalMenu

def generate_menu(title, items):
	menu_title = title
	menu_items = items

	menu = TerminalMenu(
		menu_entries = menu_items,
		title = menu_title,
		menu_cursor = "-> ",
		menu_cursor_style = ("fg_blue","bold"),
		menu_highlight_style = ("bg_black", "fg_blue"),
		cycle_cursor = True,
		#show_shortcut_hints = True,
		exit_on_shortcut = False,
		#clear_screen =True,
	)

	selection_index = menu.show()
	#print(selection_index)
	#print(menu.chosen_accept_key)
	#print(menu.chosen_menu_entries)
	return selection_index
