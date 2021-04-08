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
Data Carving command generation.
requires a path to carve, output path and the name of the Dir
"""
def DC_commmand_gen(conf_path, tool, dir_name, carve_path):
	command = 'sudo {} '.format(tool)
	if tool == 'foremost':
		command += '-T -v -c {} {} -o {}'.format(conf_path, carve_path, dir_name)
	if tool == 'scalpel':
		command += '-v -c {} {} -o {}/'.format(conf_path, carve_path, dir_name)
	return command

"""
pdfid command generation, creates a command the identify any objects in a pdf file
outputs a txt file to the same location as the PDF
requires a path, settings check for disarming, and file
"""
def PDF_pdfid_command_gen(path, d_check, filename):
	command = 'sudo pdfid '
	if d_check == 'True':
		command += '-d '
	new_filename = filename.split('.')
	txt = open(path + new_filename[0] + '_pdfid.txt', 'w')
	txt.write('')
	txt.close()
	command += path + filename + ' -o ' + path + new_filename[0] + '_pdfid.txt'
	return command

"""
Pdf parser reads the objects of a pdf file and displays its content.
generates a command to write output to a txt file in the same location
returns the created command
"""
def PDF_pdfparser_objs_command_gen(path, filename):
	command = 'sudo pdf-parser -c -O ' + path + filename		#-c contents
	new_filename = filename.split('.')				#-f filter
	command += ' > ' + path + new_filename[0] + '_parser_objs.txt'
	return command

"""
Pdf parser reads the objects of a pdf file and displays its content.
generates a command to identify what objects are in what streams and returns that output to a txt file
returns the created command
"""
def PDF_pdfparser_locs_command_gen(path, filename):
	command = 'sudo pdf-parser -a -O ' + path + filename
	new_filename = filename.split('.')
	command += ' > ' + path + new_filename[0] + '_parser_locs.txt'
	return command

"""
pdf parser reads the pdf file and prints a txt file containing a md5 hash for each object.
if the .pdf cannot be hashed, then the file will contain zero hashes.
returns the created command
"""
def PDF_pdfparser_hash_command_gen(path, filename):
	new_filename = filename.split('.')
	command = 'sudo pdf-parser -H ' + path + filename
	command += ' > ' + path + new_filename[0] + '_parser_md5.txt'
	return str(command)






