#Python DC_Controller (Data Carving)
#Desc: Handles all of the operations within the application realting to Data Carving

import click
import sys
import os

from View import MainMenu_Controller
from Model.ScalpelSetting import ScalpelSetting
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms
from Scripts import ScalpelSettingsScript as sss
from Scripts import CommandCreationScript as ccs
from Scripts import FdiskScript as fds
from Scripts import UsageLoggingScript as uls

"""
DC_main_menu is first page requsts the user to select tool.
NOTE: AS OF KALI V2020.4 For The Pi4. SCALPLE DOES NOT FUNCTION WITHOUT TROUBLESHOOTING
"""
def DC_main_menu():
	os.system('clear')
	click.secho('Data Carving (Scalpel): Scalpel Type\n', fg='blue', bold=True)
	click.echo('There are mutiple tools to perform data_carving. that perform different functions')

	click.secho('*AS OF KALI V2020.4 For The Pi4. SCALPLE DOES NOT FUNCTION WITHOUT TROUBLESHOOTING\n', fg='red', bold=True)
	click.echo('If The User Wishes To Troubleshoot Themsleves, Then Scalple Will Proceed To Function Correctly')
	
	choices = ['[1] Foremost (.dd/ .img/ .RAW)','[2] Scalpel (*/ Files/ Connected Drives)','[3] PhotoRec (Indipendent Program)','[4] Main Menu']
	title = '\nPlease Select A Tool'

	index_selection = tms.generate_menu(title, choices)

	if index_selection == 0:
		DC_selection('foremost')
	elif index_selection == 1:
		DC_selection('scalpel')
	elif index_selection == 2:
		DC_photorec_selection()
	elif index_selection == 3:
		MainMenu_Controller.main_menu()

	MainMenu_Controller.main_menu()
	
	
"""
DC_selection, Select carve type selection for scalpel
if the tool selected is scalpel, it will prompt the user to ask for either a file or drive
else it will ignore and continue to acqure a file
generates data required for the DC_conform function
"""
def DC_selection(tool):
	os.system('clear')
	click.secho('Data Carving (Scalpel): Scalpel Type', fg='blue', bold=True)

	if tool == 'scalpel':					#prompt if scalpel
		title = '\nWhat Would You Like To Carve?'
		choices = ['[1] Connected Drive','[2] Acquired Img File','[0] Back']
		conf_path = scs.settings_check('$Scalpel_ConfFile_Location')
		index_selection = tms.generate_menu(title, choices)
	else:
		index_selection = 1
		conf_path = scs.settings_check('$Foremost_ConfFile_Location')

	choices = []
	path = ''	
	if index_selection == 0:
		drive_path = DC_selection_drive(path, tool)				#get drive
		selected_settings_list = DC_config(conf_path)
		dir_name = DC_selection_dir()					#generate a list of scalpelsetting classes
		DC_conform(selected_settings_list, conf_path, dir_name, tool, drive_path)
	elif index_selection == 1:
		img_path = DC_selection_image(tool)				#get file
		selected_settings_list = DC_config(conf_path)				
		dir_name = DC_selection_dir()
		DC_conform(selected_settings_list, conf_path, dir_name, tool, img_path)
	elif index_selection == 2:
		DC_main_menu()
	else:
		DC_main_menu()

"""
configuration menu for DC. 
generates a list(class(ScalpelSetting)) based on user input)
requires the conf filepath for either foremost or scalpel
returns a altered list(class(ScalpelSetting)) containing the options to enable/disable
"""
def DC_config(conf_path):
	os.system('clear')
	click.secho('Data Carving: Config', fg='blue', bold=True)

	click.echo('\nThis will edit and select Different File Types in the .conf file')
	click.echo('Conf file found under: ' + conf_path)
	click.echo('If You Are unsure What This Means, Please Refer to The file Above For More Information')

	click.echo('\nCurrently Saved Options Under Catergories:')
	settings_list = sss.get_DC_settings_list(conf_path)				#generate a class list of scalple settings	
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
	elif index_selection == 1 or index_selection == 2:
		for setting in settings_list:
			for option in setting.get_options():				#reset all old options
				option[0] = '#'
		new_settings_list = DC_Wizard(index_selection, settings_list, conf_path)	#gen new list via wizard
		return new_settings_list
	elif index_selection == 3:
		DC_main_menu()

	MainMenu_Controller.main_menu()

"""
DC conformation page.
displays all settings and actions to the user aswell as the command.
warning with 2 second prompt window
"""
def DC_conform(selected_settings_list, conf_path, dir_name, tool, img_path):
	os.system('clear')
	click.secho('Data Carving: Conform\n', fg='blue', bold=True)

	click.secho('Selected Data Carving Tool: ', bold=True)
	click.echo(tool)
	click.secho('Selected Drive/File To Carve: ', bold=True)
	click.echo(img_path)
	click.secho('Selected Output Location:', bold=True)
	click.echo('ForinApp/')
	click.secho('Selected Output Dir Name:\n', bold=True)
	click.echo(scs.settings_check('$DC_Output_Location_Name'))

	files = ''
	all_files = ''
	for count, setting in enumerate(selected_settings_list):	#display settings that user selected
		if files != '':
			click.echo(files.strip())
		files = ''
		check = count
		for option in setting.get_options():
			if option[0] == '@' and check == count:
				check = check + 1
				click.secho(setting.get_cat().strip(), bold=True)
			if option[0] == '@':
				files += option[1] + ', '
				all_files += option[1] + ', '
	else:
		if files != '':
			click.echo(files.strip())		

	click.secho('\n- --- - WARNING - --- - --- - WARNING - --- - --- - WARNING - --- -', fg='red', bold=True)
	click.secho('Changes will be made to the scalpel.conf file', bold = True)

	click.secho('\nCOMMAND:', bold=True)
	command = ccs.DC_commmand_gen(conf_path, tool, dir_name, img_path)			#generate scalple command
	click.echo(command)
	title = '\nYou Are About To Execute The Above Command Do You With To Proceed?'
	index_selection = tms.generate_promt_menu(title, 2)				#prompt

	if index_selection == 0:
		DC_main_menu()
	elif index_selection == 1:
		uls_filepath = scs.settings_check('$Default_UsageLog_Location')
		if uls_filepath.endswith('/') == False:
			uls_filepath += '/'
		uls_filepath += 'Dc_Usage_Logs.txt'
		uls.log_change(uls_filepath, 'Data_Carve_Attempt', ((command + '\n'), (all_files + '\n\n')))

		old_txt = list(sss.get_DC_settings_txt(conf_path))				#save old settings
		new_txt = list(sss.get_DC_settings_txt(conf_path))
		new_txt = sss.create_DC_settings_txt(new_txt, selected_settings_list)
		sss.set_DC_settings_txt(new_txt, conf_path)
		os.system('clear')
		os.system(command)					#EXECUTE
		sss.set_DC_settings_txt(old_txt, conf_path)					#write old settings
		wait_selection = tms.generate_menu('\nOperation Complete. Please Press Enter To Continue: ENTER', [' '])

	MainMenu_Controller.main_menu()

"""
DC wizards, contains 2 wizards that display setting either by catergory or file.
uses script to generate a multi_select window that returns a list(str(selection))
requires a menu_selection check and a list(ScalpelSetting)
returns list(Altered: ScalpelSetting)
"""
def DC_Wizard(menu_selection, settings_list, conf_path):
	os.system('clear')
	click.secho('Data Carving: File Type Selection', fg='blue', bold=True)

	click.echo('\nIf custom options are added to the .conf file, they will be detected')

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

	new_settings_list = sss.set_DC_settings_list(settings_list, index_selection, check)	 #scalple script call

	if type(new_settings_list) != list:
		DC_config(conf_path)

	return new_settings_list

"""
Directory Selection Page, asks the user to select a path.
generates a sting_menu based on option selected if required.
returns a directory path for carve output
"""
def DC_selection_dir():
	os.system('clear')
	click.secho('Data Carving: Dir/Folder Name', fg='blue', bold=True)

	settings_list = scs.get_settings_list()
	name = scs.settings_check('$DC_Output_Location_Name')						#get saved Dir name
	click.echo('\nCurrently Saved Name: {} (will format name if dir already exsists)'.format(name))

	choices = []
	for setting in settings_list:
		if setting.get_code_call() == '$DC_Output_Location_Name':
			for choice in setting.get_items_list():
				choices.append(choice)

	choices.append('[1] Use Default: {}'.format(name))
	choices.append('[0] Back')
	title = '\nPlease Select The Name Of The Directory Where The Evidence Will Be Stored:'
	
	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		DC_main_menu()
	elif choices[index_selection].startswith('--') == True:
		name = tms.generate_string_menu(setting.get_code_call() == '$DC_Output_Location_Name', 0)	#gen string menu
	else:
		pass	

	return name
	
"""
DC selection drive for scalpel tool.
uses the fdisk script similer to ACQ to gather drive information
returns a path of the selected drive/partition
requires a str (can be empty) and a tool code
"""
def DC_selection_drive(drive_path, tool):
	os.system('clear')
	click.secho('Data Carving (Scalpel): Drive Selection\n', fg='blue', bold=True)

	click.echo('Scalpel Has The Ability To Carve From Drives Connected To The Device')

	title = 'Please Select a Drive'
	drives = fds.fdisk(False, False)		#gather info of connected drives
	choices = []
	check = 1
	for drive in drives:
		if drive.get_boot() == True and scs.settings_check('$Boot_Drive_Override') == 'True':
			choices.append('[{}] {}'.format(check, drive.get_path()))
			check = check + 1
		elif drive.get_boot() == False:
			choices.append('[{}] {}'.format(check, drive.get_path()))
			check = check + 1
	choices.append('[0] Back')

	index_selection = tms.generate_menu(title, choices)		#select drive

	if index_selection == len(choices) - 1:
		DC_main_menu()

	if scs.settings_check('$Boot_Drive_Override') == 'False':
		dc_drive = drives[index_selection + 1]
	else:
		dc_drive = drives[index_selection]

	choices = ['[1] Full Drive']
	for part in dc_drive.get_partitions():
		choices.append(part.split(':')[0])
	choices.append('[0] Back')

	index_selection = tms.generate_menu(title, choices)	#select partition

	if index_selection == len(choices) - 1:
		DC_selection(tool)

	if index_selection == 0:
		sel_drive_path = dc_drive.get_path()
	else:
		sel_drive_path = choices[index_selection]

	return sel_drive_path			#return drive/part path
	 
"""
DC image selection page, requires the user the select a img file to carve.
requires a file path to where the files are located
returns a full path with file_path + name
"""
def DC_selection_image(tool, path=scs.settings_check('$Default_Output_Location')):
	os.system('clear')
	click.secho('Data Carving: Image Selection', fg='blue', bold=True)

	click.echo('Currently Selected Evidance Path: {}'.format(path))

	choices = []
	title = '\nWhat Would You Like To Carve?\nIf You Dont See Any Files Try Specifying a Custom Path In The Settings'	#get files at output loc
	for file in os.listdir(path):
		if file.lower().endswith('.dd') or file.lower().endswith('.img') or file.lower().endswith('.raw') or file.lower().endswith('.aff'):
			choices.append(file)
	choices.append('[0] Back')

	index_selection = tms.generate_menu(title, choices)
	
	if index_selection == len(choices) - 1:
		DC_main_menu()
	else:
		img_file_name = choices[index_selection]
		return path + str(img_file_name)

"""
photorec selection page, is a prompt page asking the user if the wish to procced
"""
def DC_photorec_selection():
	os.system('clear')
	click.secho('Data Carving: PhotoRec\n', fg='blue', bold=True)

	click.echo('PhotoRec is a powerful data recovery tool similer to the others in this program')
	click.echo('However, PhotoRec Takes Advanatge of its own Wizard')

	click.secho('\nWARNING: PhotoRec Will Be Run As SU', fg='red')

	title = '\nWould You Like To Procced ToUse PhotoRec?'
	choices = ['[1] Lauch PhotoRec', '[0] Back']

	index_selection = tms.generate_menu(title, choices)

	if index_selection == 0:
		os.system('sudo photorec')
	else:
		DC_main_menu()
	
	MainMenu_Controller.main_menu()
	
