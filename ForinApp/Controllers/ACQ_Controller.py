#Python ACQ_Controller (Acquisition)
#Desc: Handles all of the operations within the application realting to acquisition

import click
import sys
import os
import numpy as np

#Import Drive Class
from Classes.Drive import Drive

from Scripts import ErrorScript as es
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms

"""
Drive Selection Page
Calls Function To Read fidsk command output from file
Stores selected Drive deatils and the partition selected
Boot_override check to avoid imaging boot drive
"""
def ACQ_selection():
	os.system('clear')

	click.secho('1.1: Device Selection', fg='blue', bold=True)
	click.echo('\nWRITE BLOCKER:  Disabled')
	click.echo('DEVICE SEARCH: "fdisk -l"')
	click.echo('NOTE: 1 Is Usually Your Boot Drive. Please Double Check To Confirm Yourself')

	read_storage_file()		#Function call to detect connected drives
	
	choices = []
	for count, drive in enumerate(detected_drives):				#global var gen'd by func
		choices.append('[{}] {}'.format(count + 1, drive.get_path()))
	choices.append('[0] Back')
	title = '\nPlease select the drive you would like to acquire.'

	drive_selected = False
	global ACQ_drive

	#drive selection
	x = True
	while x == True:
		index_selection = tms.generate_menu(title, choices)
		for count, drive in enumerate(detected_drives):
			try:
				if count == index_selection:
					drive_selected = True
					if index_selection == bootdrive_code:	#check if boot
						check = scs.settings_check('Boot_Drive_Override')
						if check == 'False':
							es.error(1002, 0)
						elif check == 'True':
							ACQ_drive = drive					
							x = False
							break
						else:
							es.error(1003, 1)
					else:
						ACQ_drive = drive
						x = False
						break
			except:
				continue
		if index_selection == (len(choices) - 1):
			#main_header()
			click.echo('Go Back To main Menu')
		elif drive_selected == False:
			es.error(1001, 0)

	choices = []
	choices.append('[1] Full Drive')
	for count, section in enumerate(ACQ_drive.get_partitions()):
		choices.append('[{}] {}'.format(count + 2, ACQ_drive.get_drive_partition(count)))
	choices.append('[0] Back')
	title = '\nPlease select the drive you would like to acquire.'

	#partition Selection
	partition_selected = False

	x = True
	while x == True:
		index_selection = tms.generate_menu(title, choices)

		if index_selection == 0:
			ACQ_drive.set_partition_selection(ACQ_drive.get_path())
			ACQ_config()
			break
		elif index_selection == (len(choices) - 1):
			click.echo('menu')
		else:
			try:
				for count, partition in enumerate(ACQ_drive.get_partitions()):
					if count == index_selection:
						ACQ_drive.set_partition_selection(ACQ_drive.get_drive_partition(count - 1))
						partition_selected = True
						x = False
						break				
				if partition_selected == True:
					ACQ_config()
					x = False
					break
				else:
					es.error(1000, 0)
					x = False
					break
			except:
					es.error(1000, 0)

"""
Configuration Selection Page
2x config files are created based on which tool will be used (dc3dd/dcfldd)
"""
def ACQ_config():
	os.system('clear')

	click.secho('1.2: Acquisition Configuration', fg='blue', bold=True)

	config1, config2 = load_default_ACQ_conf()			#returned configs

	choices = ['[1] Use Default Configuration', '[2] Use Custom Configuration (Wizard)', 
		'[3] Quick Acquire (No hashing or Logging)', '[0] Back']
	title = '\nPlease select the drive you would like to acquire.'

	#config selection
	x = True
	while x == True:
		index_selection = tms.generate_menu(title, choices)

		if index_selection == 0:
			check = scs.settings_check('Default_Tool')	#settings file check
			click.echo(check)
			if check == 'dc3dd':
				ACQ_conform(config1)
				break
			elif check == 'dcfldd':
				ACQ_conform(config2)
				break
		elif index_selection == 1:
			ACQ_wizard(config1, config2)
			break
		elif index_selection == 2:
			config1[0] = 'dc3dd' 
			config1[2] = 'False' 
			config1[4] = 'False'
			ACQ_conform(config1)
			break
		elif index_selection == (len(choices) - 1):
			ACQ_selection()
			break
		else:
			es.error(1000, 0)

"""
Conformation page
Loads and displays selected config based on previous slection or custom selections
Creates and executes command based on tool (With Warning)
"""
def ACQ_conform(config):
	os.system('clear')
	click.secho('1.3: Acqusition Conformation',bold=True, fg='blue')

	click.secho('\nDrive To Aquire Details:', bold=True)
	click.echo('Drive Path: {}'.format(ACQ_drive.get_path()))
	click.echo('Partition to Aquire: {}'.format(ACQ_drive.get_partition_selection()))
	click.echo('Drive Size: GB: {} / Bytes: {}'.format(ACQ_drive.get_size_gb(), ACQ_drive.get_size_bytes()))
	
	click.secho('\nSettings Specified:', bold=True)
	
	if config[0] == 'dc3dd':						#Load config for 'dc3dd'
		click.echo('Acqusition Tool: {}'.format(config[0]))		#config1 = [0 - tool, 1 - output_location, 2 - hashing,
		click.echo('\nOutput_Location: {}'.format(config[1]))			#3 - hashing_mode, 4 - logging, 5 - logging_location]
		click.echo('Enable_OTF_Hashing: {}'.format(config[2]))
		if config[2] == 'True':
			click.echo('Hashing_Mode: {}'.format(config[3]))
		click.echo('Enable_Logging: {}'.format(config[4]))
		if config[4] == 'True':
			click.echo('Logging_Location: {}'.format(config[5]))

	elif config[0] == 'dcfldd':						#Load Config for 'dcfldd'
		click.echo('Acqusition Tool: {}'.format(config[0]))		#config2 = [0 - tool, 1 - output_location, 2 - hashing, 3 - logging, 
		click.echo('\nOutput_Location: {}'.format(config[1]))			#4 - logging_location, 5 - multiple_hashing, 6 - Hashing_mode_1, 
		click.echo('Enable Logging: {}'.format(config[3]))			#7 - hashing_mode_2, 8 - byte_split, 9 - file_splitting, 
		if config[3] == 'True':							#10 - split_size, 11 - split_format, 12 - hash_window, 13 - hash_converstion]
			click.echo('Logging_Location: {}'.format(config[4]))
		click.echo('Enable_OTF_Hashing: {}'.format(config[2]))
		if config[2] == 'True':
			click.echo('Hashing_Mode 1: {}'.format(config[6]))
			click.echo('Enable Multiple Hashes: {}'.format(config[5]))
		if config[5] == 'True':
			click.echo('Hashing_Mode 2: {}'.format(config[7]))
		click.echo('Byte Split: {}'.format(config[8]))
		click.echo('Enable File Splitting: {}'.format(config[9]))
		if config[9] == 'True':
			click.echo('Split Size: {}'.format(config[10]))
			click.echo('Split Format: {}'.format(config[11]))
			click.echo('Hashing Window: {}'.format(config[12]))
		click.echo('Hash Conversion: {}'.format(config[13]))

	#File Ext. generator / file name generator
	img = str(ACQ_drive.get_partition_selection())
	a, b, name = img.split('/')

	ext = '_00'

	count = 1
	while True:
		filepath = '{}{}{}{}'.format(scs.settings_check('Default_Output_Location'), name, ext, str(count))
		if (os.path.isfile(filepath + '.img') == True and config[0] == 'dc3dd'):
			count = count + 1
		elif (os.path.isfile(filepath + '.dd') == True and config[0] == 'dcfldd'):
			count = count + 1
		else:
			name += (ext + str(count))
			break

	#Command Creation for 'dc3dd'
	if config[0] == 'dc3dd':
		line = ''
		command = 'sudo dc3dd'
		command += ' if={}'.format(str(ACQ_drive.get_partition_selection()))
		command += ' of={}{}.img'.format(config[1], name)
		if config[2] == 'True':
			command += ' hash={}'.format(config[3])
		if config[4] == 'True':
			command += ' log={}{}.log'.format(config[5], name) 

	#command creation for 'dcfldd'
	elif config[0] == 'dcfldd':
		a = ''
		b = ''
		command = 'sudo dcfldd'
		command += ' if={}'.format(str(ACQ_drive.get_partition_selection()))
		if config[2] == 'True':
			command += ' hash={}'.format(config[6])
			a = ' {}log={}{}_{}.txt'.format(config[6], config[4], name, config[6])
			if config[5] == 'True':
				command += ',{}'.format(config[7])
				b = ' {}log={}{}_{}.txt'.format(config[7], config[4], name, config[7])
		command += a
		command += b
		command += ' hashconv={}'.format(config[13])
		command += ' bs={}'.format(config[8])
		command += ' hashwindow={}'.format(config[12])
		if config[9] == 'True':
			command += ' split={}'.format(config[10])
			command += ' splitformat={}'.format(config[11])
		command += ' of={}{}.dd'.format(config[1], name)

	click.secho('\n- --- - WARNING - --- -', bold=True, fg='red')
	click.echo('\nCommand: {}'.format(command))
	click.secho('\nYou Are About To Execute The Above Command! Do You Wish To Proceed? [Y/N]', bold=True)

	#warning selection
	choices = ['[1] TERMINATE!', '[2] EXECUTE!']
	index_selection = tms.generate_menu('', choices)

	if index_selection == 1:
		os.system(command)
	else:
		ACQ_config()
		
"""
Wizard page
2x Wizards based on the tool the user uses
"""
def ACQ_wizard(config1, config2):

	#Wizard For 'dc3dd'
	def ACQ_wizard1(config1):
		config = config1

		choices = ['[1] Default: {}'.format(config[1]), '[2] Internal: Evidence/', '[0] Back']
		title = '\nPlease Select An Output Path'

		#path selection with '.isdir' check.
		x = True
		while x == True:
			index_selection = tms.generate_menu(title, choices)
			check = os.path.isdir(config[1])
			tmp = config[1]
			if check == True and index_selection == 0:
				if tmp[-1:] != '/':
					tmp += str('/')
				config[1] = tmp
				click.echo('"{}" Selected'.format(config[1]))
				break	
			else:
				if index_selection == 1:
					config[1] = 'Evidence/'
					click.echo('"{}" Selected'.format(config[1]))
					break
				elif selection == 2:
					ACQ_config()
					break
				else:
					es.error(1004, 0)
		
		choices = ['[1] Default: {}'.format(config[3]), '[2] md5', '[3] sha1', '[4] sha256',
			 '[5] sha512', '[6] None (Disable)', '[0] Back']
		title = '\nPlease Specify On-The-Fly Hashing Algorithm:'

		#hash selection
		x = True
		while x == True:
			index_selection = tms.generate_menu(title, choices)

			if index_selection == 0:
				click.echo('{} Selected'.format(config[3]))
				break
			elif index_selection == 1:
				config[3]  = 'md5'
				click.echo('{} Selected'.format(config[3]))
				break
			elif index_selection == 2:
				config[3]  = 'sha1'
				click.echo('{} Selected'.format(config[3]))
				break
			elif index_selection == 3:
				config[3]  = 'sha256'
				click.echo('{} Selected'.format(config[3]))
				break
			elif index_selection == 4:
				config[3]  = 'sha512'
				click.echo('{} Selected'.format(config[3]))
				break
			elif index_selection == 5:
				config[2]  = 'False'
				click.echo('On-The-Fly Hasing Disabled')
				break
			elif index_selection == 6:
				ACQ_config()
				break
			else:
				es.error(1000, 0)

		choices = ['[1] Default: {}'.format(config[5]), '[2] Internal: Logs/', '[3] None (Disable)' '[0] Back']
		title = '\nPlease Specify A Output Path For The Log Files:'

		#log file selection with '.isdir' check
		x = True
		while x == True:
			index_selection = tms.generate_menu(title, choices)
			check = os.path.isdir(config[5])
			tmp = config[5]
			if check == True and index_selection == 0:
				if tmp[-1:] != '/':
					tmp += str('/')
				config[5] = tmp
				click.echo('"{}" Selected'.format(config[5]))
				break		
			else:
				if index_selection == 1:
					config[5] = 'Logs/'
					click.echo('Logs/ Selected')
					break
				elif index_selection == 2:
					click.echo('Logging Disabled')
					config[4] = 'False'
					break
				elif index_selection == 3:
					ACQ_config()
					break
				else:
					es.error(1004, 0)

		ACQ_conform(config)

	#(Advanced) Wizard for 'dcfldd'
	def ACQ_wizard2(config2):
		config = config2

		choices = ['[1] Default: {}'.format(config[1]), '[2] Internal: Evidence/', '[0] Back']
		title = '\nPlease Select An Output Path'

		#path selection with '.isdir' check.
		x = True
		while x == True:
			index_selection = tms.generate_menu(title, choices)
			check = os.path.isdir(config[1])
			tmp = config[1]
			if check == True and index_selection == 0:
				if tmp[-1:] != '/':
					tmp += str('/')
				config[1] = tmp
				click.echo('"{}" Selected'.format(config[1]))
				break	
			else:
				if index_selection == 1:
					config[1] = 'Evidence/'
					click.echo('"{}" Selected'.format(config[1]))
					break
				elif selection == 2:
					ACQ_config()
					break
				else:
					es.error(1004, 0)

		choices = ['[1] Default: {}'.format(config[6]), '[2] md5', '[3] sha1', '[4] sha256',
			 '[5] sha512', '[6] None (Disable)', '[0] Back']
		title = '\nPlease Specify On-The-Fly Hashing Algorithm:'

		#hash selection
		x = True
		while x == True:
			index_selection = tms.generate_menu(title, choices)

			if index_selection == 0:
				click.echo('{} Selected'.format(config[6]))
				break
			elif index_selection == 1:
				config[6]  = 'md5'
				click.echo('{} Selected'.format(config[6]))
				break
			elif index_selection == 2:
				config[6]  = 'sha1'
				click.echo('{} Selected'.format(config[6]))
				break
			elif index_selection == 3:
				config[6]  = 'sha256'
				click.echo('{} Selected'.format(config[6]))
				break
			elif index_selection == 4:
				config[6]  = 'sha512'
				click.echo('{} Selected'.format(config[6]))
				break
			elif index_selection == 5:
				config[2]  = 'False'
				click.echo('On-The-Fly Hasing Disabled')
				break
			elif index_selection == 6:
				ACQ_config()
				break
			else:
				es.error(1000, 0)
		
		if config[2] != 'False':	
			choices = ['[1] Default: {}'.format(config[6]), '[2] md5', '[3] sha1', '[4] sha256',
			 	'[5] sha512', '[6] None (Disable)', '[0] Back']
			title = '\nPlease Specify 2nd On-The-Fly Hashing Algorithm:'

			#2nd hash selection
			x = True
			while x == True:
				index_selection = tms.generate_menu(title, choices)
				if index_selection == 0:
					click.echo('{} Selected'.format(config[7]))
					break
				elif index_selection == 1:
					config[7]  = 'md5'
					click.echo('{} Selected'.format(config[7]))
					break
				elif index_selection == 2:
					config[7]  = 'sha1'
					click.echo('{} Selected'.format(config[7]))
					break
				elif index_selection == 3:
					config[7]  = 'sha256'
					click.echo('{} Selected'.format(config[7]))
					break
				elif index_selection == 4:
					config[7]  = 'sha512'
					click.echo('{} Selected'.format(config[7]))
					break
				elif index_selection == 5:
					config[5]  = 'False'
					click.echo('On-The-Fly Hasing Disabled')
					break
				elif index_selection == 6:
					ACQ_config()
					break
				else:
					es.error(1000, 0)

		choices = ['[1] Default: {}'.format(config[5]), '[2] Internal: Logs/', '[3] None (Disable)', '[0] Back']
		title = '\nPlease Specify A Output Path For The Log Files:'

		#log file selection with '.isdir' check
		x = True
		while x == True:
			index_selection = tms.generate_menu(title, choices)
			check = os.path.isdir(config[4])
			tmp = config[4]
			if check == True and index_selection == 0:
				if tmp[-1:] != '/':
					tmp += str('/')
				config[4] = tmp
				click.echo('"{}" Selected'.format(config[4]))
				break		
			else:
				if index_selection == 1:
					config[4] = 'Logs/'
					click.echo('Logs/ Selected')
					break
				elif index_selection == 2:
					click.echo('Logging Disabled')
					config[3] = 'False'
					break
				elif index_selection == 3:
					ACQ_config()
					break
				else:
					es.error(1004, 0)

		choices = ['[1] Default: {}'.format(config[8]), '[2] 256', '[3] 512', '[4] 1024', '[5] 2048', '[0] Back']
		title = '\nPlease Sepcify A Byte Split (Read x Sectors Then Write)'

		#byte split selection
		x = True
		while x == True:
			index_selection = tms.generate_menu(title, choices)
			if index_selection == 0:
				click.echo('{} Selected'.format(config[8]))
				break
			elif index_selection == 1:
				config[8]  = '256'
				click.echo('{} Selected'.format(config[8]))
				break
			elif index_selection == 2:
				config[7]  = '512'
				click.echo('{} Selected'.format(config[7]))
				break
			elif index_selection == 3:
				config[7]  = '1024'
				click.echo('{} Selected'.format(config[7]))
				break
			elif index_selection == 4:
				config[7]  = '2048'
				click.echo('{} Selected'.format(config[7]))
				break
			elif index_selection == 5:
				ACQ_config()
				break
			else:
				es.error(1000, 0)

		choices = ['[1] Default: {}'.format(config[10]), '[2] 1G', '[3] 2G', '[4] 5G', 
			'[5] 10G', '[6] 20G', '[7] None (Disable)', '[0] Back']
		title = '\nSplit Image File? (Gb) (Hash Window Will Copy This Selection)'

		#img splitting selection
		x = True
		while x == True:
			index_selection = tms.generate_menu(title, choices)
			if index_selection == 0:
				click.echo('{} Selected'.format(config[10]))
				config[12] = config[10]
				break
			elif index_selection == 1:
				config[10]  = '1G'
				click.echo('{} Selected'.format(config[10]))
				config[12] = config[10]
				break
			elif index_selection == 2:
				config[10]  = '2G'
				click.echo('{} Selected'.format(config[10]))
				config[12] = config[10]
				break
			elif index_selection == 3:
				config[10]  = '5G'
				click.echo('{} Selected'.format(config[10]))
				config[12] = config[10]
				break
			elif index_selection == 4:
				config[10]  = '10G'
				click.echo('{} Selected'.format(config[10]))
				config[12] = config[10]
				break
			elif index_selection == 5:
				config[10]  = '20G'
				click.echo('{} Selected'.format(config[10]))
				config[12] = config[10]
				break
			elif index_selection == 6:
				config[9]  = 'False'
				click.echo('File Splitting Disabled')
				break
			elif index_selection == 7:
				ACQ_config()
				break
			else:
				es.error(1000, 0)

		if config[9] != 'False':
			choices = ['[1] Default: {}'.format(config[11]), '[2] nnn (img.012)', '[3] aaa (img.abc)', 
					'[4] ann (img.a01)', '[0] Back']
			title = '\nPlease Specify A Split File Format:'

			#split format selection
			x = True
			while x == True:
				index_selection = tms.generate_menu(title, choices)
				if index_selection == 0:
					click.echo('{} Selected'.format(config[11]))
					break
				elif index_selection == 1:
					config[11] = 'nnn'
					click.echo('{} Selected'.format(config[11]))
					break
				elif index_selection == 2:
					config[11] = 'aaa'
					click.echo('{} Selected'.format(config[11]))
					break
				elif index_selection == 3:
					config[11] = 'ann'
					click.echo('{} Selected'.format(config[11]))
					break
				elif index_selection == 4:
					ACQ_config()
					break
				else:
					es.error(1000, 0)

		choices = ['[1] After', '[2] Before', '[0] Back']
		title = '\nPeform Hash Befor Or After Converstion:'
		#hashconv selection
		x = True
		while x == True:
			index_selection = tms.generate_menu(title, choices)
			if index_selection == 0:
				config[13] = 'after'
				click.echo('{} Selected'.format(config[13]))
				break
			elif index_selection == 1:
				config[13] = 'before'
				click.echo('{} Selected'.format(config[13]))
				break
			elif index_selection == 2:
				ACQ_config()
				break
			else:
				es.error(1000, 0)

		ACQ_conform(config)

	os.system('clear')
	click.secho('1.2.1: Acqusition Configuration Wiazrd', fg='blue', bold=True)
	
	choices = ['[1] dc3dd (.img Files)', '[2] dcfldd (.dd Files) (Advanced)', '[0] Back']
	title = '\nPWhat Tool Would You Like To Use?'

	#wizard selection
	x = True
	while x == True:
		index_selection = tms.generate_menu(title, choices)
		if index_selection == 0:
			ACQ_wizard1(config1)
			break
		elif index_selection == 1:
			ACQ_wizard2(config2)
			break
		elif index_selection == 2:
			ACQ_config()
			break
		else:
			es.error(1000, 0)

"""
Read storage file command
reads a storage file name Storage.txt under /config
String handling to store the only needed infomation based on patterns in the Storage.txt file.
"""
def read_storage_file():
	drive_found = False		
	details = ''
	found_drives = []				
	drive_count = 0
	found_sections = [] 
	global detected_drives
	global bootdrive_code
	
	detected_drives = []
	os.system('sudo fdisk -l > Config/Storage.txt')

	txt = open('Config/Storage.txt','r')
	txt_lines = txt.readlines()

	for line in txt_lines:
		if line[0:6] == 'Disk /':		#check for disk line
			if line.find('ram') != -1:	#Ignore Ram
				pass
			else:
				drive_found = True					
				line_count = 0
				drive_count = drive_count + 1
				details += '\nDrive {} Details:\n'.format(str(drive_count))
				details += str(line)
				found_drives.append(line)

		elif drive_found == True:
			if line == '\n':
				line_count = line_count + 1
				details += '\n'
				if line_count >= 2:
					drive_found = False			#end of drive info
					click.echo('')
			else:
				details += str(line)
				if line.find('Boot') != -1:			#Check for boot
					bootdrive_code = drive_count - 1
				if line.find('/') != -1 and line_count == 1:
					found_sections.append(line)	
	txt.close()
	click.echo(details)
	
	for count, drive in enumerate(found_drives):			#retrive stored drive String info (single 'Disk/' file line and format)
		a, path, sizeGB, b, sizeBytes, c, d, e  = drive.split(' ')
		path, a = path.split(':')
		detected_drives.append(Drive(count + 1, path, float(sizeGB), float(sizeBytes)))

	for section in found_sections:					#retrive and format String partitions
		section_path = section[:11]
		section_path = section_path.rstrip()
		for count, drive in enumerate(detected_drives):
			if section.find('{}'.format(str(drive.get_path()))) !=  -1:
				drive.add_drive_partition(section_path)

"""
function that reads the config file and returns 2 configs
uses the settings check function to gather configs
"""
def load_default_ACQ_conf():
	click.secho('\nDefault Configuration:', bold = True)	
	
	tool_check = scs.settings_check('Default_Tool')

	tool = 'dc3dd'
	output_location = scs.settings_check('Default_Output_Location')
	hashing = scs.settings_check('Enable_OTF_Hashing')
	hashing_mode = scs.settings_check('Hashing_Mode')
	logging = scs.settings_check('Enable_Logging')
	logging_location = scs.settings_check('Default_Logging_Location')
	
	config1 = [tool, output_location, hashing, hashing_mode, logging, logging_location]

	tool = 'dcfldd'
	output_location = scs.settings_check('Default_Output_Location')
	hashing = scs.settings_check('Enable_OTF_Hashing')
	logging = scs.settings_check('Enable_Logging')
	logging_location = scs.settings_check('Default_Logging_Location')
	multiple_hashing = scs.settings_check('Multiple_Hashing')
	Hashing_mode_1 = scs.settings_check('Hashing_Mode_1')
	hashing_mode_2 = scs.settings_check('Hashing_Mode_2')
	byte_split = scs.settings_check('Byte_Split')
	file_splitting = scs.settings_check('File_Splitting')
	split_size = scs.settings_check('Split_Size')
	split_format = scs.settings_check('Split_Format')
	hash_window = split_size
	hash_converstion = scs.settings_check('Hashing_Conversion')

	config2 = [tool, output_location, hashing, logging, logging_location, multiple_hashing, 
		Hashing_mode_1, hashing_mode_2, byte_split, file_splitting, split_size, 
		split_format, hash_window, hash_converstion]

	if tool_check == 'dc3dd':	
		click.echo('\nDefault Tool: {}'.format(config1[0]))
		click.echo('Default Output Location: {}'.format(config1[1]))
		click.echo('Enable On-The-Fly Hashing: {}'.format(config1[2]))
		click.echo('Hashing Mode: {}'.format(config1[3]))
		click.echo('Enable Logging: {}'.format(config1[4]))
		click.echo('Default Logging_Location: {}\n'.format(config1[5]))
	elif tool_check == 'dcfldd':
		click.echo('Default Tool: {}'.format(config2[0]))
		click.echo('Default Output Location: {}'.format(config2[1]))
		click.echo('Enable On-The-Fly Hashing: {}'.format(config2[2]))
		click.echo('Enable Logging: {}'.format(config2[3]))
		click.echo('Default Logging Location: {}'.format(config2[4]))
		if config2[2] == 'True':
			click.echo('Enable Multple Hashing: {}'.format(config2[5]))
			if config2[5] == 'True':
				click.echo('Hashing Mode 1: {}'.format(config2[6]))
				click.echo('Hashing Mode 2: {}'.format(config2[7]))
			else:
				click.echo('Hashing Mode: {}'.format(config2[6]))
		click.echo('Byte Split: {}'.format(config2[8]))
		click.echo('Enable File Splitting: {}'.format(config2[9]))
		if config2[9] ==  'True':
			click.echo('Split Size (G): {}'.format(config2[10]))
			click.echo('Split Format (aaa, nnn): {}'.format(config2[11]))
			click.echo('Hashing Window: {}'.format(config2[12]))
		click.echo('Hash Converstion: {}'.format(config2[13]))
	else:
		ErrorScript.error(1003, 2)

	return config1, config2

