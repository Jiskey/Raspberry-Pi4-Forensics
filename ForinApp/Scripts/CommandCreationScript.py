#Python Command Creation Script
#Used whenever the app requries a specific and complex teminal window user command needs to be created

import sys
import os

from Scripts import SettingsCheckScript as scs

"""
Data Carving command generation.
requires a path to carve, output path and the name of the Dir
"""
def DC_commmand_gen(conf_path, tool, dir_name, carve_path):
	command = 'sudo {} '.format(tool)
	if tool == 'foremost':
		command += '-T -v -c {} {} -o {}/'.format(conf_path, carve_path, dir_name)
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
	new_filename = filename.split('.')				#discard contents of file
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






