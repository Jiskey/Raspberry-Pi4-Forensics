#Python ACQ_Controller (Acquisition)
#Desc: Handles all of the operations within the application realting to acquisition

import click
import sys
import os
import numpy as np

#Import Drive Class
from Classes.Drive import Drive

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

	#Function call to detect connected drives
	read_storage_file()	
	
	for count, drive in enumerate(detected_drives):
		click.echo('{} - {}'.format(count + 1, drive.get_path()))	
	
	click.echo('0 - Back')		

	click.echo('\nPlease select the drive you would like to acquire.')
	drive_selected = False
	global ACQ_drive

	#drive selection
	x = True
	while x == True:
		selection = input('\n--- ')
		for count, drive in enumerate(detected_drives):
			try:
				if count == int(selection) - 1:
					drive_selected = True
					if int(selection) == bootdrive_code:
						check = settings_check('Boot_Drive_Override')
						if check == 'False':
							error(1002, 0)
						elif check == 'True':
							ACQ_drive = drive					
							x = False
							break
						else:
							error(1003, 1)
					else:
						ACQ_drive = drive
						x = False
						break
			except:
				continue
		if selection == '0':
			#main_header()
			click.echo('Go Back To main Menu')
			break
		elif drive_selected == False:
			error(1001, 0)

	click.echo('\nPlease select the partition you would like to aquire:')
	click.echo('1 - Full Drive')
	for count, section in enumerate(ACQ_drive.get_partitions()):
		click.echo('{} - {}'.format(count+ 2, ACQ_drive.get_drive_partition(count)))
	click.echo('0 - Back')

	partition_selected = False
	#partition Selection
	x = True
	while x == True:
		selection = input('\n--- ')

		if selection == '1':
			ACQ_drive.set_partition_selection(ACQ_drive.get_path())
			ACQ_config()
			break
		elif selection == '0':
			click.echo('menu')
		else:
			try:
				for count, partition in enumerate(ACQ_drive.get_partitions()):
					if count == int(selection) - 2:
						ACQ_drive.set_partition_selection(ACQ_drive.get_drive_partition(count))
						partition_selected = True
						x = False
						break				
				if partition_selected == True:
					ACQ_config()
					x = False
					break
				else:
					error(1000, 0)
					x = False
					break
			except:
					error(1000, 0)

"""
Configuration Selection Page
2x config files are created based on which tool will be used (dc3dd/dcfldd)
"""
def ACQ_config():
	os.system('clear')

	click.secho('1.2: Acquisition Configuration', fg='blue', bold=True)
	
	#returned configs
	config1, config2 = load_default_ACQ_conf()

	click.echo('\n1. Use Default Configuration')
	click.echo('2. Use Custom Configuration (Wizard)')
	click.echo('3. Quick Acquire (No hashing or Logging)')
	click.echo('0. Back')

	#config selection
	x = True
	while x == True:
		selection = input('\n--- ')

		if selection == '1':
			check = settings_check('Default_Tool')
			click.echo(check)
			if check == 'dc3dd':
				ACQ_conform(config1)
				break
			elif check == 'dcfldd':
				ACQ_conform(config2)
				break
		elif selection == '2':
			ACQ_wizard(config1, config2)
			break
		elif selection == '3':
			config1[0] = 'dc3dd' 
			config1[2] = 'False' 
			config1[4] = 'False'
			ACQ_conform(config1)
			break
		elif selection == '0':
			ACQ_selection()
			break
		else:
			error(1000, 0)
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
	
	#Load config for 'dc3dd'
	if config[0] == 'dc3dd':
		#config1 = [tool, output_location, hashing, hashing_mode, logging, logging_location]
		click.echo('Acqusition Tool: {}'.format(config[0]))
		click.echo('\nOutput_Location: {}'.format(config[1]))
		click.echo('Enable_OTF_Hashing: {}'.format(config[2]))
		if config[2] == 'True':
			click.echo('Hashing_Mode: {}'.format(config[3]))
		click.echo('Enable_Logging: {}'.format(config[4]))
		if config[4] == 'True':
			click.echo('Logging_Location: {}'.format(config[5]))

	#Load Config for 'dcfldd'
	elif config[0] == 'dcfldd':
		#config2 = [0 - tool, 1 - output_location, 2 - hashing, 3 - logging, 
			#4 - logging_location, 5 - multiple_hashing, 6 - Hashing_mode_1, 
			#7 - hashing_mode_2, 8 - byte_split, 9 - file_splitting, 
			#10 - split_size, 11 - split_format, 12 - hash_window, 13 - hash_converstion]
		click.echo('Acqusition Tool: {}'.format(config[0]))
		click.echo('\nOutput_Location: {}'.format(config[1]))
		click.echo('Enable Logging: {}'.format(config[3]))
		if config[3] == 'True':
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

	click.echo('\nPlease Specify a Name For The Image:')
	click.echo('\n0. Back')		

	#img name selection
	img_name = input('\n--- ')
	if img_name == '0':
		ACQ_config()

	#Command Creation for 'dc3dd'
	if config[0] == 'dc3dd':
		line = ''
		command = 'sudo dc3dd'
		command += ' if={}'.format(str(ACQ_drive.get_partition_selection()))
		command += ' of={}{}.img'.format(config[1], img_name)
		if config[2] == 'True':
			command += ' hash={}'.format(config[3])
		if config[4] == 'True':
			command += ' log={}{}.log'.format(config[5], img_name) 

	#command creation for 'dcfldd'
	elif config[0] == 'dcfldd':
		a = ''
		b = ''
		command = 'sudo dcfldd'
		command += ' if={}'.format(str(ACQ_drive.get_partition_selection()))
		if config[2] == 'True':
			command += ' hash={}'.format(config[6])
			a = ' {}log={}{}_{}.txt'.format(config[6], config[4], img_name, config[6])
			if config[5] == 'True':
				command += ',{}'.format(config[7])
				b = ' {}log={}{}_{}.txt'.format(config[7], config[4], img_name, config[7])
		command += a
		command += b
		command += ' hashconv={}'.format(config[13])
		command += ' bs={}'.format(config[8])
		command += ' hashwindow={}'.format(config[12])
		if config[9] == 'True':
			command += ' split={}'.format(config[10])
			command += ' splitformat={}'.format(config[11])
		command += ' of={}{}.dd'.format(config[1], img_name)

	click.secho('\n- --- - WARNING - --- -', bold=True, fg='red')
	click.echo('\nCommand: {}'.format(command))
	click.secho('\nYou Are About To Execute The Above Command! Do You Wish To Proceed? [Y/N]', bold=True)

	#warning selection
	selection = input('\n--- ')
	if selection == 'y' or selection == 'Y':
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
		click.echo('\nCurrent Path: ../ForinApp/')

		click.echo('\nPlease Specify A Output Path For Evidence (Full Path or ./[dir]) or select a option:')
		click.echo('1. Use Default ({})'.format(config[1]))
		click.echo('0. Back')

		#path selection with '.isdir' check.
		x = True
		while x == True:
			selection = input('\n--- ')
			check = os.path.isdir(selection)
			if check == True:
				if selection[-1:] != '/':
					selection += str('/')
				config[1] = selection
				click.echo('"{}" Selected'.format(config[1]))
				break	
			else:
				if selection == '1':
					click.echo('"{}" Selected'.format(config[1]))
					break
				elif selection == '0':
					ACQ_config()
					break
				else:
					error(1004, 0)

		click.echo('\nPlease Specify On-The-Fly Hashing Algorithm:')
		click.echo('1. Use Default ({})'.format(config[3]))
		click.echo('2. md5')
		click.echo('3. sha1')
		click.echo('4. sha256')
		click.echo('5. sha512')
		click.echo('6. None  (Disable)')
		click.echo('0. back')

		#hash selection
		x = True
		while x == True:
			selection = input('\n--- ')

			if selection == '1':
				click.echo('{} Selected'.format(config[3]))
				break
			elif selection == '2':
				config[3]  = 'md5'
				click.echo('{} Selected'.format(config[3]))
				break
			elif selection == '3':
				config[3]  = 'sha1'
				click.echo('{} Selected'.format(config[3]))
				break
			elif selection == '4':
				config[3]  = 'sha256'
				click.echo('{} Selected'.format(config[3]))
				break
			elif selection == '5':
				config[3]  = 'sha512'
				click.echo('{} Selected'.format(config[3]))
				break
			elif selection == '6':
				config[2]  = 'False'
				click.echo('On-The-Fly Hasing Disabled')
				break
			elif selection == '0':
				ACQ_config()
				break
			else:
				error(1000, 0)
		
		click.echo('\nPlease Specify A Output Path For The Log File (Full Path or ./[dir]) or select a option:')
		click.echo('1. Use Default ({})'.format(config[5]))
		click.echo('2. None (Disable)')
		click.echo('0. Back')

		#log file selection with '.isdir' check
		x = True
		while x == True:
			selection = input('\n--- ')
			check = os.path.isdir(selection)
			if check == True:
				if selection[-1:] != '/':
					selection += str('/')
				config[5] = selection
				click.echo('"{}" Selected'.format(config[5]))
				break		
			else:
				if selection == '1':
					click.echo('"{}" Selected'.format(config[5]))
					#ACQ_conform(config)
					break
				elif selection == '2':
					click.echo('Logging Disabled')
					config[4] = 'False'
					break
				elif selection == '0':
					ACQ_config()
					break
				else:
					error(1004, 0)

		ACQ_conform(config)

	#(Advanced) Wizard for 'dcfldd'
	def ACQ_wizard2(config2):
		config = config2
		click.echo('\nCurrent Path: ../ForinApp/')

		click.echo('\nPlease Specify A Output Path For Evidence (Full Path or ./[dir]) or select a option:')
		click.echo('1. Use Default ({})'.format(config[1]))
		click.echo('0. Back')

		#path selection with '.isdir' check.
		x = True
		while x == True:
			selection = input('\n--- ')
			check = os.path.isdir(selection)
			if check == True:
				if selection[-1:] != '/':
					selection += str('/')
				config[1] = selection
				click.echo('"{}" Selected'.format(config[1]))
				break	
			else:
				if selection == '1':
					click.echo('"{}" Selected'.format(config[1]))
					break
				elif selection == '0':
					ACQ_config()
					break
				else:
					error(1004, 0)

		click.echo('\nPlease Specify On-The-Fly Hashing Algorithm:')
		click.echo('1. Use Default ({})'.format(config[6]))
		click.echo('2. md5')
		click.echo('3. sha1')
		click.echo('4. sha256')
		click.echo('5. sha512')
		click.echo('6. None  (Disable)')
		click.echo('0. back')

		#hash selection
		x = True
		while x == True:
			selection = input('\n--- ')
			if selection == '1':
				click.echo('{} Selected'.format(config[6]))
				break
			elif selection == '2':
				config[6]  = 'md5'
				click.echo('{} Selected'.format(config[6]))
				break
			elif selection == '3':
				config[6]  = 'sha1'
				click.echo('{} Selected'.format(config[6]))
				break
			elif selection == '4':
				config[6]  = 'sha256'
				click.echo('{} Selected'.format(config[6]))
				break
			elif selection == '5':
				config[6]  = 'sha512'
				click.echo('{} Selected'.format(config[6]))
				break
			elif selection == '6':
				config[2]  = 'False'
				click.echo('On-The-Fly Hasing Disabled')
				break
			elif selection == '0':
				ACQ_config()
				break
			else:
				error(1000, 0)
		
		if config[2] != 'False':
			click.echo('\nPlease Specify A 2nd Algorithm:')
			click.echo('1. Use Default ({})'.format(config[7]))
			click.echo('2. md5')
			click.echo('3. sha1')
			click.echo('4. sha256')
			click.echo('5. sha512')
			click.echo('6. None  (Use Single Hash)')
			click.echo('0. back')
		
			#2nd hash selection
			x = True
			while x == True:
				selection = input('\n--- ')
				if selection == '1':
					click.echo('{} Selected'.format(config[7]))
					break
				elif selection == '2':
					config[7]  = 'md5'
					click.echo('{} Selected'.format(config[7]))
					break
				elif selection == '3':
					config[7]  = 'sha1'
					click.echo('{} Selected'.format(config[7]))
					break
				elif selection == '4':
					config[7]  = 'sha256'
					click.echo('{} Selected'.format(config[7]))
					break
				elif selection == '5':
					config[7]  = 'sha512'
					click.echo('{} Selected'.format(config[7]))
					break
				elif selection == '6':
					config[5]  = 'False'
					click.echo('Single Hash Selected (Multiple hashing Disabled)')
					break
				elif selection == '0':
					ACQ_config()
					break
				else:
					error(1000, 0)

		click.echo('\nPlease Specify A Output Path For The Log File (Full Path or ./[dir]) or select a option:')
		click.echo('1. Use Default ({})'.format(config[4]))
		click.echo('2. None (Disable)')
		click.echo('0. Back')

		#log file selection with '.isdir' check
		x = True
		while x == True:
			selection = input('\n--- ')
			check = os.path.isdir(selection)
			if check == True:
				if selection[-1:] != '/':
					selection += str('/')
				config[4] = selection
				click.echo('"{}" Selected'.format(config[4]))
				break		
			else:
				if selection == '1':
					click.echo('"{}" Selected'.format(config[4]))
					break
				elif selection == '2':
					click.echo('Logging Disabled')
					config[3] = 'False'
					break
				elif selection == '0':
					ACQ_config()
					break
				else:
					error(1004, 0)

		click.echo('\nPlease Sepcify A Byte Split (Read x Sectors Then Write)')
		click.echo('1. Use Default ({})'.format(config[8]))
		click.echo('2. 256')
		click.echo('3. 512')
		click.echo('4. 1024')
		click.echo('5. 2048')
		click.echo('0. Back')

		#byte split selection
		x = True
		while x == True:
			selection = input('\n--- ')
			if selection == '1':
				click.echo('{} Selected'.format(config[8]))
				break
			elif selection == '2':
				config[8]  = '256'
				click.echo('{} Selected'.format(config[8]))
				break
			elif selection == '3':
				config[7]  = '512'
				click.echo('{} Selected'.format(config[7]))
				break
			elif selection == '4':
				config[7]  = '1024'
				click.echo('{} Selected'.format(config[7]))
				break
			elif selection == '5':
				config[7]  = '2048'
				click.echo('{} Selected'.format(config[7]))
				break
			elif selection == '0':
				ACQ_config()
				break
			else:
				error(1000, 0)

		click.echo('\nSplit Image File? (Gb) (Hash Window Will Copy This Selection)')
		click.echo('1. Use Default ({})'.format(config[10]))
		click.echo('2. 1G')
		click.echo('3. 2G')
		click.echo('4. 5G')
		click.echo('5. 10G')
		click.echo('6. 20G')
		click.echo('7. Disable')
		click.echo('0. Back')

		#img splitting selection
		x = True
		while x == True:
			selection = input('\n--- ')
			if selection == '1':
				click.echo('{} Selected'.format(config[10]))
				config[12] = config[10]
				break
			elif selection == '2':
				config[10]  = '1G'
				click.echo('{} Selected'.format(config[10]))
				config[12] = config[10]
				break
			elif selection == '3':
				config[10]  = '2G'
				click.echo('{} Selected'.format(config[10]))
				config[12] = config[10]
				break
			elif selection == '4':
				config[10]  = '5G'
				click.echo('{} Selected'.format(config[10]))
				config[12] = config[10]
				break
			elif selection == '5':
				config[10]  = '10G'
				click.echo('{} Selected'.format(config[10]))
				config[12] = config[10]
				break
			elif selection == '6':
				config[10]  = '20G'
				click.echo('{} Selected'.format(config[10]))
				config[12] = config[10]
				break
			elif selection == '7':
				config[9]  = 'False'
				click.echo('File Splitting Disabled')
				break
			elif selection == '0':
				ACQ_config()
				break
			else:
				error(1000, 0)

		if config[9] != 'False':
			click.echo('\nPlease Specify A Split File Format:')
			click.echo('1. Use Default ({})'.format(config[11]))			
			click.echo('2. nnn (img.012)')
			click.echo('3. aaa (img.abc)')
			click.echo('4. ann (img.a01)')
			click.echo('0. Back')

			#split format selection
			x = True
			while x == True:
				selection = input('\n---')
				if selection == '1':
					click.echo('{} Selected'.format(config[11]))
					break
				elif selection == '2':
					config[11] = 'nnn'
					click.echo('{} Selected'.format(config[11]))
					break
				elif selection == '3':
					config[11] = 'aaa'
					click.echo('{} Selected'.format(config[11]))
					break
				elif selection == '4':
					config[11] = 'ann'
					click.echo('{} Selected'.format(config[11]))
					break
				elif selection == '0':
					ACQ_config()
					break
				else:
					error(1000, 0)

		click.echo('\nPeform Hash Befor Or After Converstion:')
		click.echo('1. Use Default ({})'.format(config[13]))
		click.echo('2. After')
		click.echo('3. Before')
		click.echo('0. Back')

		#hashconv selection
		x = True
		while x == True:
			selection = input('\n--- ')
			if selection == '1':
				click.echo('{} Selected'.format(config[13]))
				break
			elif selection == '2':
				config[13] = 'after'
				click.echo('{} Selected'.format(config[13]))
				break
			elif selection == '3':
				config[13] = 'before'
				click.echo('{} Selected'.format(config[13]))
				break
			elif selection == '0':
				ACQ_config()
				break
			else:
				error(1000, 0)

		ACQ_conform(config)

	os.system('clear')
	click.secho('1.2.1: Acqusition Configuration Wiazrd', fg='blue', bold=True)
	
	click.secho('\nWhat Tool Would You Like To Use?', bold=True)
	click.echo('1. dc3dd')
	click.echo('2. dcfldd (Advanced)')
	click.echo('0. Back')

	#wizard selection
	x = True
	while x == True:
		selection = input('\n--- ')
		
		if selection == '1':
			ACQ_wizard1(config1)
			break
		elif selection == '2':
			ACQ_wizard2(config2)
			break
		elif selection == '0':
			ACQ_config()
			break
		else:
			error(1000, 0)

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
		#check for disk line
		if line[0:6] == 'Disk /':
			#ignore ram
			if line.find('ram') != -1:
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
					drive_found = False
					click.echo('')
			else:
				details += str(line)
				if line.find('Boot') != -1:
					bootdrive_code = drive_count
				if line.find('/') != -1 and line_count == 1:
					found_sections.append(line)	
	txt.close()
	click.echo(details)
	
	#retrive stored drive info (single 'Disk/' file line and format)
	for count, drive in enumerate(found_drives):
		a, path, sizeGB, b, sizeBytes, c, d, e  = drive.split(' ')
		path, a = path.split(':')
		detected_drives.append(Drive(count + 1, path, float(sizeGB), float(sizeBytes)))

	#retrive and format partitions
	for section in found_sections:
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
	
	tool = 'dc3dd'
	output_location = settings_check('Default_Output_Location')
	hashing = settings_check('Enable_OTF_Hashing')
	hashing_mode = settings_check('Hashing_Mode')
	logging = settings_check('Enable_Logging')
	logging_location = settings_check('Default_Logging_Location')
	
	config1 = [tool, output_location, hashing, hashing_mode, logging, logging_location]

	tool = 'dcfldd'
	output_location = settings_check('Default_Output_Location')
	hashing = settings_check('Enable_OTF_Hashing')
	logging = settings_check('Enable_Logging')
	logging_location = settings_check('Default_Logging_Location')
	multiple_hashing = settings_check('Multiple_Hashing')
	Hashing_mode_1 = settings_check('Hashing_Mode_1')
	hashing_mode_2 = settings_check('Hashing_Mode_2')
	byte_split = settings_check('Byte_Split')
	file_splitting = settings_check('File_Splitting')
	split_size = settings_check('Split_Size')
	split_format = settings_check('Split_Format')
	hash_window = split_size
	hash_converstion = settings_check('Hashing_Conversion')

	config2 = [tool, output_location, hashing, logging, logging_location, multiple_hashing, Hashing_mode_1, hashing_mode_2, byte_split, file_splitting, split_size, split_format, hash_window, hash_converstion]

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
		error(1003, 2)

	return config1, config2

"""
Settings check function that reads the settings file under Config/
returns the setting selected in the settings file by reading the file
"""
def settings_check(setting):
	txt = open('Config/Settings.txt', 'r')
	txt_lines = txt.readlines()	

	for line in txt_lines:
		if line.find(setting) != -1:
			line = line.rstrip('\n')
			name, statement = line.split(':')
			txt.close()
			return statement
			break
		else:
			pass

	txt.close()

"""
Error Handling
Codes used to select the error with optional tags for similer errors
"""
def error(code, tag):
	#1000: Invalid Seletion General Error
	if code == 1000:
		click.echo('Error: Invalid Selection. Please select a Valid option.')
	#1001: Wrong Drive Selection
	if code == 1001:
		click.echo('Error: No Drive Detected, Please Select Valid Drives.')
	#1002: Same Drive Acquisition & Storage Attempt
	if code == 1002:
		click.echo('Error: Cannot Aquire The Boot Drive Of This Device')
		click.echo('Hint: Override Disable in Settings.txt under Config/Settings.txt [Boot_Drive_Overide:True]')
	#1003: Settings File Fatal Error: Unable To Read Statement
	if code == 1003:
		click.echo('Settings.txt File Fatal Error: Unable To Read Statement')
		if tag == 1:
			click.echo('Error On Line: Boot_Drive_Override')
		if tag == 2:
			click.echo('Error On Line: Default_Tool')
	#1004: Unable To varify selected Directory
	if code == 1004:
		click.echo('Unable to verify directory. please select a valid Directory')
	

