#Python ACQ_Controller (Acquisition)
#Application Name: Forin
#Author: J.Male
#Desc: 
#	Handles all of the operations within the application realting to acquisition.
#	uses Tools Dcfldd/dc3dd to perfom such actions. *as of kali 2021.1 These tool are notincluded by default

import click
import sys
import os
import time

from Model.AcqDrive import AcqDrive	
from View import MainMenu_Controller
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms
from Scripts import FdiskScript as fds
from Scripts import UsageLoggingScript as uls

"""
ACQ_selection First Page.
Runs a creates a drive list by calling fdisk script and displays none verbose to user
Lets User Select a Drive and/or Partition
"""
def ACQ_selection():
	acq_drive = AcqDrive					
	p_code = 255
	choices = []
	check = 1
	title = ''

	os.system('clear')
	click.secho('Acquisition: Drive Selection', fg='blue', bold=True)
	click.secho('\nAcquisition Allows You Collect A Forensic Image File (filename.dd) From Connect Drive.', bold=True)
	click.echo('Connected Device Search: "fdisk -l".')
	click.echo('Note: If Boot Override is Set To: False. "Boot" Drives Will Not Be Selectable.')
	click.echo('Boot Drive Override: {}'.format(scs.settings_check('$Boot_Drive_Override')))
	click.echo('Below Are The Found Drives Connected To This Device.\n')

	drives_list = fds.fdisk(False)
	try:
		### Connected Drive Choices
		for count, drive in enumerate(drives_list):
			if drive.get_boot() == True and scs.settings_check('$Boot_Drive_Override') == 'True':
				choices.append('[{}] {}'.format(check, drive.get_path()))
				check = check + 1
			elif drive.get_boot() == False:	
				choices.append('[{}] {}'.format(check, drive.get_path()))
				check = check + 1
	except:
		click.echo('Error Reading Drives!')

	choices.append('[0] Main Menu')
	title = ('Please Select The Drive You Would like To Acquire')

	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		MainMenu_Controller.main_menu()
	
	### Acquired Drive Partition Choices
	for drive in drives_list:
		choice_path = choices[index_selection].split()
		if choice_path[1].strip() == drive.get_path().strip():
			acq_drive = drive

	choices = ['[1] Full Drive']
	for count, parts in enumerate(acq_drive.get_partitions()):
		choices.append('[{}] {}'.format(count + 2, parts.split(':')[0]))
	choices.append('[0] Back')
	title = 'Please Select The Partition You Would Like To Acquire'			

	index_selection = tms.generate_menu(title, choices)		

	if index_selection == len(choices) - 1:
		ACQ_selection()
	if index_selection == 0:
		p_code = 255
	else:
		p_code = index_selection - 1

	ACQ_config(acq_drive, p_code)

"""
Configuration Page, User Can Select Different Options To Change Settings.
Contains a Wizard, Load Default From Settings.txt and custom config function (hard coded)
ACQ_wizard Returns a Altered Settings_List
Requires The Drive To Acquire and The Partition Code
"""
def ACQ_config(acq_drive, p_code):
	try:
		settings_list = scs.get_settings_list()
		new_settings_list = []
		check = 0
		choices = ['[1] Use Default Configuration', '[2] Use Custom Configuration (Wizard)', 
			'[3] Quick Acquire (No hashing or Logging)', '[0] Back']
		title = '\nPlease Choose A Configuration'
	except:
		title = '\nError Loading Settings File! Please Get A Replacement OR check Config/Settings.txt'
		choices = ['[0] Back']

	os.system('clear')
	click.secho('Acquisition: Configuration\n', fg='blue', bold=True)
	click.echo('You Can Either Select The Currently Saved Settings Or Quick Config.\nOR Use the Wizard To Specify Some Custom Settings.')
	click.echo('\nRecommended/Simple Acqusition: 3. Quick Aquire')
	click.secho('\nCurrent Saved/Default Settings:', bold=True)

	###Get Current Settings From Settings List
	try:
		for setting in settings_list:
			if setting.get_section() == '----- Acqusisition Settings -----':
				new_settings_list.append(setting)			
				call, var = setting.get_code().split(':')
				if check < 7:						
					check = check + 1
					click.echo('{} -- {}'.format(call[1:], var))
				elif settings_list[0].get_code_var() == 'dcfldd':
					click.echo('{} -- {}'.format(call[1:], var))
	except:
		click.echo('Error Loading Settings File! Returning To Main Menu. Please Get A Replacement OR check Config/Settings.txt')
		time.sleep(3)
		MainMenu_Controller.main_menu()
		sys.exit(0)
		

	index_selection = tms.generate_menu(title, choices)

	if index_selection == 0:						
		ACQ_conform(new_settings_list, acq_drive, p_code)
	elif index_selection == 1:						
		new_settings_list = ACQ_wizard(new_settings_list, acq_drive, p_code)
		ACQ_conform(new_settings_list, acq_drive, p_code)
	elif index_selection == 2:						
		new_settings_list = ACQ_config_quick(new_settings_list)
		ACQ_conform(new_settings_list, acq_drive, p_code)
	elif index_selection == 3:
		ACQ_selection()

"""
Conformation page, Loads and displays selected config based on previous selection or custom selections
Generates a command based on the required items
Requires a settings list, a drive to acquire and the partition code (int(255) == Full Drive)
After Command Execution, Usage_Log Is Recorded
"""
def ACQ_conform(settings_list, acq_drive, p_code):
	command = acq_drive.gen_command(settings_list, p_code)
	skip_items = []
	check = False

	### Display Selected Drive Information
	os.system('clear')
	click.secho('Acquisition: Execution\n', fg='blue', bold=True)
	click.secho('Below Is The Details Of The Drive To Acquire & The Settings Selected!', bold=True)
	click.echo('Note: A Image File MAY Be Larger Then The Actuall Drive Size! Ensure Enough Storage Space Is Avalible!\n')
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

	### Print Selected Tool Settings
	click.secho('Selected Settings:', bold=True)
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

	### Prompt User, Print Command, Freeze 2 Second
	click.secho('\n- --- - WARNING - --- - --- - WARNING - --- - --- - WARNING - --- -', fg='red', bold=True)
	click.echo('\nNOTE: Please Check To Ensure That All Settings Are Correct And The Generated Command Is Correct')
	click.echo('If You Are Unsure Of The Configuration Or Unsure What A Setting Does, Please Proceed With Caution')
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
		uls.log_change(logfile, 'Acq_Attempt', command + '\n')			
		os.system(command)							### EXECUTE
		wait_selection = tms.generate_menu('Operation Complete. Please Press Enter To Continue: ENTER', [' '])

	MainMenu_Controller.main_menu()
	 
"""
Wizard Config Page, Cycles through the list of ACQ settings
Requires a settings list, a drive to acquire and the partition code (int(255) == Full Drive)
returns a new settings_list based on selections in the wizard
"""
def ACQ_wizard(settings_list, acq_drive, p_code):
	choices = []
	title = ''
	skip_menus = []
	list_dels = []
	tool_code = ''

	### Cycle Through Whole Settings List
	for count, setting in enumerate(settings_list):			
		os.system('clear')
		click.secho('Acquisition: Automatic Wizard\n', fg='blue', bold=True)
		click.secho('Please Select An Option You Would Like For Each Setting!', bold=True)
		click.secho('Options With "--" Require A Custom String Output\n')

		### Collect Current Setting
		choices = []
		title = setting.get_description()
		for choice in setting.get_items_list():
			choices.append(choice)
		choices.append('[1] Use Default: {}'.format(scs.settings_check(setting.get_code_call())))
		choices.append('[0] Back')			

		### Skip Menus Based On User Input / Setting Selection
		if setting.get_code_call() == '$Multiple_Hashing' and tool_code == 'dc3dd':	
			settings_list = settings_list[:count]
			break

		skip = False						
		for skip_code in skip_menus:
			if skip_code == setting.get_code_call():
				skip = True
		if skip == True:
			list_dels.append(count)				
			continue
		elif skip == False:
			index_selection = tms.generate_menu(title, choices)		

		if index_selection == len(choices) - 1 or index_selection == '0':	
			ACQ_config(acq_drive, p_code)
			break

		if index_selection == len(choices) - 2:
			continue

		if choices[index_selection].startswith('--') == True:			
			title = choices[index_selection]
			if choices[index_selection] == '-- Specify New Acq File_Name':
				var = tms.generate_string_menu(title, 0)
			else:
				var = tms.generate_dir_menu()

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
			tool_code = setting.get_code_var()

	### Delete Marked Items
	check = 0					
	for del_ in list_dels:
		settings_list.pop(del_ - check)
		check = check + 1

	return settings_list

"""
custom config 'quick' sets custom settings based on selections below. (hard Coded)
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
