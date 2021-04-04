#Python DC_Controller (Data Carving)
#Desc: Handles all of the operations within the application realting to Data Carving

import click
import sys
import os

from Controllers import MainMenu_Controller
from Classes.ScalpelSetting import ScalpelSetting
from Scripts import ErrorScript as es
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms
from Scripts import ScalpelSettingsScript as sss
from Scripts import CommandCreationScript as ccs

"""
DC_selection, main menu for DATA CARVING section
"""
def DC_selection():
	os.system('clear')
	click.secho('Data Carving (Scalpel): Scalpel Type', fg='blue', bold=True)

	title = '\nWhat Would You Like To Carve?'
	choices = ['[1] Connected Drive','[2] Acquired Img File','[0] Back']
	index_selection = tms.generate_menu(title, choices)

	choices = []
	path = ''	
	if index_selection == 0:
		drive_path = DC_selection_drive(path)				#get drive
		selected_settings_list = DC_config()
		dir_name = DC_selection_dir()					#generate a list of scalpelsetting classes
		DC_conform(selected_settings_list, drive_path, dir_name)
	elif index_selection == 1:
		img_path = DC_selection_image(path)				#get file
		selected_settings_list = DC_config()				
		dir_name = DC_selection_dir()
		DC_conform(selected_settings_list, img_path, dir_name)
	elif index_selection == 2:
		MainMenu_Controller.main_menu()
	else:
		MainMenu_Controller.main_menu()

"""
configuration menu for DC. 
generates a list(class(ScalpelSetting)) based on user input)
returns a altered list(class(ScalpelSetting)) containing the options to enable/disable
"""
def DC_config():
	os.system('clear')
	click.secho('Data Carving (Scalpel): Scalpel Config', fg='blue', bold=True)

	conf_path = '/etc/scalpel/scalpel.conf'							#scalpel conf file path
	click.echo('\nThis will edit and select Different File Types in the Scalpel.conf file')
	click.echo('Conf file found under: ' + conf_path)
	click.echo('If You Are unsure What This Means, Please Refer to The file Above For Information')

	click.echo('\nCurrently Saved Options Under Catergories:')
	settings_list = sss.get_scalpel_settings_list()				#generate a class list of scalple settings	
	for setting in settings_list:
		check = 0
		for option in setting.get_options():
			if option[0] == '@' and check == 0:			#print category if theres a saved option within
				click.echo(setting.get_cat().strip())	
				check = check + 1

	title = '\nHow Would You Like To Proceed?'
	choices = ['[1] Use Currently Selected Options','[2] Simple Wizard (Type based)','[3] Advanced Wizard (Individual Files)', '[0] Back']

	index_selection = tms.generate_menu(title, choices)

	if index_selection == 0:			#use currently saved config
		return settings_list
	if index_selection == 1 or 2:
		for setting in settings_list:
			for option in setting.get_options():				#reset all old options
				option[0] = '#'
		new_settings_list = DC_Wizard(index_selection, settings_list)			#gen new list via wizard
		return new_settings_list
	if index_selection == 3:
		DC_selection()

	MainMenu_Controller.main_menu()

"""
DC conformation page.
displays all settings and actions to the user aswell as the command.
warning with 2 second prompt window
"""
def DC_conform(selected_settings_list, path, dir_name):
	os.system('clear')
	click.secho('Data Carving (Scalpel): Conform\n', fg='blue', bold=True)

	output = scs.settings_check('$DC_Output_Location')		#check for duplicate dir's
	check = 0
	for dir in os.listdir(output):
		if dir == dir_name:
			dir_name += check
			check = check + 1

	click.secho('Selected Output Location:', bold=True)
	click.echo(output)
	click.secho('Selected Output Dir Name: ', bold=True)
	click.echo(dir_name)

	cat = ''
	files = ''
	for count, setting in enumerate(selected_settings_list):	#display settings that user selected
		if files != '':
			click.echo(files + '\n')
		files = ''
		check = count
		for option in setting.get_options():
			if option[0] == '@' and check == count:
				check = check + 1
				#cat += setting.get_cat()
				click.echo(setting.get_cat().strip())
			if option[0] == '@':
				files += option[1] + ', '
	else:
		if files != '':
			click.echo(files)		

	click.secho('\n- --- - WARNING - --- - --- - WARNING - --- - --- - WARNING - --- -', fg='red', bold=True)
	click.secho('Changes will be made to the scalpel.conf file', bold = True)

	click.secho('\nCOMMAND:', bold=True)
	command = ccs.scalpel_commmand_gen(path, output, dir_name)			#generate scalple command
	click.echo(command)

	title = '\nYou Are About To Execute The Above Command Do You With To Proceed?'
	index_selection = tms.generate_promt_menu(title, 2)				#prompt

	if index_selection == 0:
		DC_selection()
	elif index_selection == 1:
		old_txt = list(sss.get_scalpel_settings_txt())				#save old settings
		new_txt = list(sss.get_scalpel_settings_txt())

		new_txt = sss.create_scalpel_settings_txt(new_txt, selected_settings_list)
		sss.set_scalpel_settings_txt(new_txt)
		os.system(command)					#EXECUTE
		sss.set_scalpel_settings_txt(old_txt)					#write old settings
	
	MainMenu_Controller.main_menu()

"""
DC wizards, contains 2 wizards that display setting either by catergory or file.
uses script to generate a multi_select window that returns a list(str(selection))
requires a menu_selection check and a list(SettingScalpel)
returns list(Altered: SettingScalpel)
"""
def DC_Wizard(menu_selection, settings_list):
	os.system('clear')
	click.secho('Data Carving (Scalpel): File Type Selection', fg='blue', bold=True)

	click.echo('\nIf custom options are added to the Scalpel.conf file, they will be detected')

	type_choices = ['[1] Select All']	
	file_choices = ['[1] Select All']					
	for setting in settings_list:
		type_choices.append(setting.get_cat().strip())				#append type selection
		for count, option in enumerate(setting.get_options()):
			file_choices.append(option[1].strip() + '  ' + option[3].strip() + '  ' + option[4].strip())	#append option selection
	type_choices.append('[0] Back')
	file_choices.append('[0] Back')	

	check = ''
	if menu_selection == 1:								#generate multi slect menu
		title = '\nPlease Select the Type Of Files You Wish to Carve'	
		title += '\nSelect "Select All" to select everything on exit or select "Back" to leave on exit\n'
		index_selection = tms.gernerate_multi_select_menu(title, type_choices, True)	#False = returns tuple of indices
		check = 'simp'
	elif menu_selection == 2:								#True = returns tuple of str's
		title = '\nPlease Select the Files You Wish to Carve'
		title += '\nSelect "Select All" to select everything on exit or select "Back" to leave on exit\n'
		title += '\n     Ext   Size   Header/Footer'
		index_selection = tms.gernerate_multi_select_menu(title, file_choices, True)
		check = 'adv'
	else:
		MainMenu_Controller.main_menu()	

	new_settings_list = sss.set_scalpel_settings_list(settings_list, index_selection, check)	 #scalple script call

	if type(new_settings_list) != list:
		DC_config()

	return new_settings_list

"""
Directory Selection Page, asks the user to select a path.
generates a sting_menu based on option selected if required.
returns a directory path for carve output
"""
def DC_selection_dir():
	os.system('clear')
	click.secho('Data Carving (Scalpel): Dir/Folder Name', fg='blue', bold=True)

	settings_list = scs.get_settings_list
	name = scs.settings_check('$DC_Output_Location_Name')						#get saved Dir name
	click.echo('\nCurrently Saved Name: {} (will format name if dir already exsists)'.format(name))

	choices = []
	for setting in settings_list():
		if setting.get_code_call() == '$DC_Output_Location_Name':
			for choice in setting.get_items_list():
				choices.append(choice)

	choices.append('[1] Use Default: {}'.format(name))
	choices.append('[0] Back')
	title = '\nPlease Select The Name Of The Directory Where The Evidence Will Be Stored:'
	
	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		DC_config()
	elif choices[index_selection].startswith('--') == True:
		name = tms.generate_string_menu(setting.get_code_call() == '$DC_Output_Location_Name', 0)	#gen string menu
	else:
		pass	

	return name
	
"""

"""
def DC_selection_drive():
	os.system('clear')
	click.secho('Data Carving (Scalpel): Drive Selection', fg='blue', bold=True)

"""
DC image selection page, requires the user the select a img file to carve.
requires a file path to where the files are located
returns a full path with file_path + name
"""
def DC_selection_image(img_path):
	os.system('clear')
	click.secho('Data Carving (Scalpel): Image Selection', fg='blue', bold=True)

	if img_path == '':
		path = scs.settings_check('$Default_Output_Location')		#get output loc
	else:
		path = img_path
	click.echo('Currently Selected Evidance Path: {}'.format(path))

	choices = []
	title = '\nWhat Would You Like To Carve?\nIf You Dont See Any Files Try Specifying a Custom Path'	#get files at output loc
	for file in os.listdir(path):
		if file.lower().endswith('.dd') or file.lower().endswith('.img') or file.lower().endswith('.raw') or file.lower().endswith('.aff'):
			choices.append(file)
	choices.append('-- Specify Other Output Location')
	choices.append('[0] Back')

	index_selection = tms.generate_menu(title, choices)
	
	if index_selection == len(choices) - 1:
		DC_selection()
	elif index_selection == len(choices) - 2:
		index_selection = tms.generate_string_menu('Data Carving File Path', 1)
		if index_selection == '0':
			DC_selection_image(img_path)
		elif index_selection.endswith('/') == False:					#append if needed
			index_selection += '/'
			DC_selection_image(index_selection)
		else:
			DC_selection_image(index_selection)
	
	img_file_name = ''
	for count, file in enumerate(os.listdir(path)):
		if count == index_selection:
			img_file_name = file
		
	return (path + img_file_name)
