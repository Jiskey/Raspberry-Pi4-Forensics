#Python ACQ_Controller (Acquisition)
#Desc: Handles all of the operations within the application realting to acquisition

import click
import sys
import os

from Classes.Drive import Drive	
from Controllers import MainMenu_Controller
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms
from Scripts import FdiskScript as fds
from Scripts import CommandCreationScript as ccs
from Scripts import UsageLoggingScript as uls
"""
First Page
Runs a script and uses tool 'fdisk' to display and create user options
saves the selected drive and the partition code
"""
def ACQ_selection():
	os.system('clear')

	click.secho('Acquisition: Drive Selection', fg='blue', bold=True)
	click.echo('\nDEVICE SEARCH: "fdisk -l"')
	click.echo('Note: If Boot Override is Set To: False. The Suspect Boot Drive Will Not Show (Can Be changed In Settings)')
	click.echo('Boot Drive Override: {}\n'.format(scs.settings_check('$Boot_Drive_Override')))

	drives_list = fds.fdisk(False)				#script Runs 'sudo fdisk' + returns list of drives

	acq_drive = Drive					
	p_code = 255						#code 255 = full drive path (no partiton)

	choices = []
	check = 1
	for count, drive in enumerate(drives_list):
		if drive.get_boot() == True and scs.settings_check('$Boot_Drive_Override') == 'True':
			choices.append('[{}] {}'.format(check, drive.get_path()))
			check = check + 1
		elif drive.get_boot() == False:						#Hide boot if false
			choices.append('[{}] {}'.format(check, drive.get_path()))
			check = check + 1
	choices.append('[0] Back')
	title = ('Please Select The Drive You Would like To Acquire')

	index_selection = tms.generate_menu(title, choices)		#Display connected Drives

	if index_selection == len(choices) - 1:
		MainMenu_Controller.main_menu()

	if scs.settings_check('$Boot_Drive_Override') == 'False':
		acq_drive = drives_list[index_selection + 1]				#save selected Drive
	else:
		acq_drive = drives_list[index_selection]

	choices = ['[1] Full Drive']
	for count, parts in enumerate(acq_drive.get_partitions()):
		choices.append('[{}] {}'.format(count + 2, parts.split(':')[0]))
	choices.append('[0] Back')
	title = 'Please Select The Partition You Would Like To Acquire'			

	index_selection = tms.generate_menu(title, choices)		#display partitions of selected drive

	if index_selection == len(choices) - 1:
		ACQ_selection()
	if index_selection == 0:
		p_code = 255
	else:
		p_code = index_selection - 1

	ACQ_config(acq_drive, p_code)
"""
Configuration page, user can select different options to change settings
contains a wizard, load default and custom config func
requires the drive to acquire and the partition code
"""
def ACQ_config(acq_drive, p_code):
	os.system('clear')
	click.secho('Acquisition: Configuration', fg='blue', bold=True)

	settings_list = scs.get_settings_list()		#get settings from settings txt
	new_settings_list = []
	new_settings_list.clear()

	click.echo('\nCurrent Saved/Default Settings:\n')
	check = 0
	for setting in settings_list:
		if setting.get_section() == '----- Acqusisition Settings -----':
			new_settings_list.append(setting)			#append needed settings
			call, var = setting.get_code().split(':')
			if check < 7:						#ignore dfcldd tools if dc3dd
				check = check + 1
				click.echo('{} -- {}'.format(call[1:], var))
			elif settings_list[0].get_code_var() == 'dcfldd':
				click.echo('{} -- {}'.format(call[1:], var))

	choices = ['[1] Use Default Configuration', '[2] Use Custom Configuration (Wizard)', 
		'[3] Quick Acquire (No hashing or Logging)', '[0] Back']
	title = '\nPlease Choose A Configuration'

	index_selection = tms.generate_menu(title, choices)

	if index_selection == 0:						#Load New Settings via Default/Saved Config
		ACQ_conform(new_settings_list, acq_drive, p_code)
	elif index_selection == 1:						#Load New settings via wizard
		new_settings_list = ACQ_wizard(new_settings_list, acq_drive, p_code)
		ACQ_conform(new_settings_list, acq_drive, p_code)
	elif index_selection == 2:						#Load New Settings via custom config
		new_settings_list = ACQ_config_quick(new_settings_list)
		ACQ_conform(new_settings_list, acq_drive, p_code)
	elif index_selection == 3:
		ACQ_selection()
"""
Conformation page
Loads and displays selected config based on previous selection or custom selections
Generates a command based on the required items
Requires a settings list, a drive to acquire and the partition code (int(255) == Full Drive)
"""
def ACQ_conform(settings_list, acq_drive, p_code):
	command = ccs.acq_command_gen(settings_list, acq_drive, p_code)
	os.system('clear')
	click.secho('Acquisition: Execution\n', fg='blue', bold=True)
	click.secho('Selected Device:', bold=True)

	click.echo('Drive To Acquire -- {}'.format(acq_drive.get_path()))					#display Drive Details
	click.echo('Drive ID -- {}'.format(acq_drive.get_identifier()))
	click.echo('Drive Size -- {}\n'.format(acq_drive.get_size()))
	
	if p_code == 255:
		click.echo('Partiton To Acquire -- {}'.format(acq_drive.get_path()))
		click.echo('Partiton Size (GB) -- {}'.format(acq_drive.get_size()))
		click.echo('Partiton Size Bytes -- {}'.format(acq_drive.get_size_bytes()))
		click.echo('Partiton Sectors -- {}\n'.format(acq_drive.get_sectors()))
	else:
		click.echo('Partiton To Acquire -- {}'.format(acq_drive.get_partition_path(p_code)))
		click.echo('Partiton Size (GB) -- {}'.format(acq_drive.get_partition_size(p_code)))
		click.echo('Partiton Size Bytes -- {}'.format(acq_drive.get_partition_size_bytes(p_code)))
		click.echo('Partiton Sectors -- {}\n'.format(acq_drive.get_partition_sectors(p_code)))

	click.secho('Selected Settings:', bold=True)
	skip_items = []
	check = False
	for count, setting in enumerate(settings_list):
		if setting.get_code_call() == '$Enable_OTF_Hashing' and setting.get_code_var() == 'False':	#skip menus based on selection
			skip_items.append('$Hashing_Mode')
			skip_items.append('$Multiple_Hashing')
			skip_items.append('$Hashing_Mode_2')
		if setting.get_code_call() == '$Enable_Logging' and setting.get_code_var() == 'False':
			skip_items.append('$Default_Hash_Logging_Location')
		if setting.get_code_call() == '$Multiple_Hashing' and setting.get_code_var() == 'False':
			skip_items.append('$Hashing_Mode_2')
		if setting.get_code_call() == '$File_Splitting' and setting.get_code_var() == 'False':
			skip_items.append('$Split_Size')
			skip_items.append('$Split_Format')

		if setting.get_code_call() == '$Multiple_Hashing':
			check = True

		skip_check = False
		for skip in skip_items:
			if skip == setting.get_code_call():		
				skip_check = True

		if skip_check == True:
			continue
				
		call, var = setting.get_code().split(':')
		if settings_list[0].get_code_var() == 'dc3dd' and check != True:				#display Settings Selected
			click.echo('{} -- {}'.format(call[1:], var))
		elif settings_list[0].get_code_var() == 'dcfldd':
			click.echo('{} -- {}'.format(call[1:], var))

	click.echo('\nNOTE: Please Check To Ensure That All Settings Are Correct And The Generated Command Is Correct')
	click.echo('If You Are Unsure Of The Configuration Or Unsure What A Setting Does, Please Proceed With Caution')

	click.secho('\n- --- - WARNING - --- - --- - WARNING - --- - --- - WARNING - --- -', fg='red', bold=True)
	click.secho('\nCOMMAND:', bold=True)
	click.echo(command)

	title = '\nYou Are About To Execute The Above Command Do You With To Proceed?'
	index_selection = tms.generate_promt_menu(title, 2)
	
	if index_selection == 0:
		ACQ_config(acq_drive, p_code)
	elif index_selection == 1:
		logfile = scs.settings_check('$Default_UsageLog_Location')
		if logfile.endswith('/') == False:
			logfile += '/'
		logfile += 'Acq_Usage_Logs.txt'
		uls.log_change(logfile, 'Acq_Attempt', command + '\n')			#update usage logs
		os.system(command)							#execute command

	MainMenu_Controller.main_menu()
	 
"""
Wizard Config Page
Cycles through the list of ACQ settings
Requires a settings list, a drive to acquire and the partition code (int(255) == Full Drive)
returns a new settings_list based on selections
"""
def ACQ_wizard(settings_list, acq_drive, p_code):
	choices = []
	title = ''
	skip_menus = []
	list_dels = []
	tool_code = ''

	for count, setting in enumerate(settings_list):			
		os.system('clear')
		click.secho('Acquisition: Automatic Wizard\n', fg='blue', bold=True)
		choices = []
		title = setting.get_description()
		for choice in setting.get_items_list():
			choices.append(choice)
		choices.append('[1] Use Default: {}'.format(scs.settings_check(setting.get_code_call())))
		choices.append('[0] Back')			

		if setting.get_code_call() == '$Multiple_Hashing' and tool_code == 'dc3dd':	#ignore dfcldd tools if dc3dd
			settings_list = settings_list[:count]
			break

		skip = False						#skip menu based on skip_menus
		for skip_code in skip_menus:
			if skip_code == setting.get_code_call():
				skip = True
		if skip == True:
			list_dels.append(count)				#store list[count] code for removal
			continue
		elif skip == False:
			index_selection = tms.generate_menu(title, choices)		#user input

		if index_selection == len(choices) - 1 or index_selection == '0':	#return to config page
			ACQ_config(acq_drive, p_code)
			break

		if index_selection == len(choices) - 2:
			continue

		if choices[index_selection].startswith('--') == True:			#detect custom string menu
			title = choices[index_selection]
			if choices[index_selection] == '--File_Name':
				code = 0
			else:
				code = 1
			var = tms.generate_string_menu(title, code)

			if var == '0':
				var = setting.get_code_call()

			setting.set_code(setting.get_code_call() + ':' + var)
		else:
			setting.set_code(setting.get_code_call() + ':' + choices[index_selection])

		if setting.get_code_call() == '$Enable_OTF_Hashing' and setting.get_code_var() == 'False':	#skip menus based on selection
			skip_menus.append('$Hashing_Mode')
			skip_menus.append('$Multiple_Hashing')
			skip_menus.append('$Hashing_Mode_2')
		if setting.get_code_call() == '$Enable_Logging' and setting.get_code_var() == 'False':
			skip_menus.append('$Default_Hash_Logging_Location')
		if setting.get_code_call() == '$Multiple_Hashing' and setting.get_code_var() == 'False':
			skip_menus.append('$Hashing_Mode_2')
		if setting.get_code_call() == '$File_Splitting' and setting.get_code_var() == 'False':
			skip_menus.append('$Split_Size')
			skip_menus.append('$Split_Format')

		if count == 0:
			tool_code = setting.get_code_var()	#save tool on first cycle (dependancy)

	check = 0					#del marked items
	for del_ in list_dels:
		settings_list.pop(del_ - check)
		check = check + 1

	return settings_list				#retun new list
"""
custom config 'quick'
sets custom settings based on selections below
Requires a settings list
returns a new settings_list
"""
def ACQ_config_quick(settings_list):
	for setting in settings_list:
		if setting.get_code_call() == '$Default_Tool':
			setting.set_code(setting.get_code_call() + ':' + setting.get_items_list()[0])
		if setting.get_code_call() == '$Enable_OTF_Hashing':
			setting.set_code(setting.get_code_call() + ':' + setting.get_items_list()[1])
		if setting.get_code_call() == '$Enable_Logging':
			setting.set_code(setting.get_code_call() + ':' + setting.get_items_list()[1])	

	return settings_list
