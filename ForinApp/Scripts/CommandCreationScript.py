#Python Command Creation Script
#Used whenever the app requries a specific and complex teminal window user command needs to bre created

import sys
import os

from Scripts import SettingsCheckScript as scs
from Classes.Drive import Drive

"""
acq_command_gen generates a command string to execute in the console
requires a list of settings, a drive to acqiure and a partition code
returns a string (command)
"""
def acq_command_gen(settings_list, acq_drive, p_code):		#p_code of 255 == full drive 
	tool = ''						#load all options due to dependence on one another
	name = ''
	output_loc = ''
	otf_hashing = ''
	hash_mode = ''
	enable_logs = ''
	hash_log_loc = ''
	multi_hash = ''
	hash_mode_2 = ''
	byte_split = ''
	file_split = ''
	split_size = ''
	split_format = ''
	hash_conv = ''
	error = ''

	for count, setting in enumerate(settings_list):
		if setting.get_code_call() == '$Default_Tool':
			tool = setting.get_code_var()
		elif setting.get_code_call() == '$Default_Image_Name':
			name = setting.get_code_var()
		elif setting.get_code_call() == '$Default_Output_Location':
			output_loc = setting.get_code_var()
		elif setting.get_code_call() == '$Enable_OTF_Hashing':
			otf_hashing = setting.get_code_var()
		elif setting.get_code_call() == '$Enable_Logging':
			enable_logs = setting.get_code_var()
		elif setting.get_code_call() == '$Hashing_Mode':
			hash_mode = setting.get_code_var()
		elif setting.get_code_call() == '$Default_Hash_Logging_Location':
			hash_log_loc = setting.get_code_var()
		elif setting.get_code_call() == '$Multiple_Hashing':
			multi_hash = setting.get_code_var()
		elif setting.get_code_call() == '$Hashing_Mode_2':
			hash_mode_2 = setting.get_code_var()
		elif setting.get_code_call() == '$Byte_Split':
			byte_split = setting.get_code_var()
		elif setting.get_code_call() == '$File_Splitting':
			file_split = setting.get_code_var()
		elif setting.get_code_call() == '$Split_Size':
			split_size = setting.get_code_var()
		elif setting.get_code_call() == '$Split_Format':
			split_format = setting.get_code_var()
		elif setting.get_code_call() == '$Hashing_Conversion':
			hash_conv = setting.get_code_var()
		elif setting.get_code_call() == '$Error_handling':
			error = setting.get_code_var()

	check = 0
	for count, file in enumerate(os.listdir(output_loc)):			#if file with same name
		if file == name + '.img':
			check = check + 1
			name = name + '_' + str(check)
	
	if hash_log_loc.endswith('/') == False:					#append loc str with /
		hash_log_loc += '/'
	if output_loc.endswith('/') == False:	
		output_loc += '/'

	start = 'sudo {} '.format(tool)						#start of command
	if p_code == 255:
		part = acq_drive.get_path()					#check partition
	else:
		part = acq_drive.get_partition_path(p_code)
	drive = 'if={} '.format(part)
	output = 'of={}'.format(output_loc)
	if output.endswith('/'):
		output += name + '.img '
	else: 
		output += '/' + name + '.img '
	if otf_hashing == 'True':
		hashing = 'hash={} '.format(hash_mode)
	else:
		hashing = ''
	if enable_logs == 'True' and otf_hashing == 'True':			#check of logging == True
		log = 'log={}{}.log '.format(hash_log_loc, name)	
	else:
		log = ''

	#gen dc3dd command
	command = start + drive + output + hashing + log

	if tool == 'dcfldd':
		if multi_hash == 'True' and hash_mode_2 != hash_mode:		#display x2 hashes
			hashing = hash_mode + ',' + hash_mode_2 + ' '
			if enable_logs == 'True':
				log = '{}log={}{}_{}.txt '.format(hash_log_loc, hash_mode, name, hash_mode)
				log += '{}log={}{}_{}.txt '.format(hash_log_loc, hash_mode_2, name, hash_mode_2)
			else:
				log = ''
		elif multi_hash == 'True' and hash_mode_2 == hash_mode:		#display x1 if a == b
			if enable_logs == 'True':
				log = '{}log={}_{}.txt '.format(hash_mode, name, hash_mode)
			else:
				log = ''
		elif multi_hash == 'False':					#display x1 if 1 hash
			if enable_logs == 'True':
				log = '{}log={}_{}.txt '.format(hash_mode, name, hash_mode)
			else:
				log = ''

		if file_split == 'True': 
			splitting = 'split={} '.format(split_size)
			splitting_format = 'splitformat={} '.format(split_format)
			hash_window = 'hashwindow={} '.format(split_size)
		else:
			splitting = ''
			splitting_format = ''
			hash_window = ''

		if error == 'True':						#error handling
			error_handling = 'conv=noerror,sync '
		else:
			error_handling = ''
		converstion = 'hashconv={} '.format(hash_conv)
		block_size = 'bs={} '.format(byte_split)	

		#gen dcfldd command
		command = start + drive + hashing + log + hash_window + converstion + block_size + error_handling + splitting + splitting_format + output
	
	return command

"""
Scalpel command generation.
requires a path to carve, output path and the name of the Dir
"""
def scalpel_commmand_gen(path, output, dir_name):
	if output.endswith('/') == False:
		output += '/' 
	command = 'sudo scalpel {} -o {}{}'.format(path, output, dir_name)
	return command
