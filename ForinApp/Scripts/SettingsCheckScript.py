import sys
import os

from Classes.Setting import Setting
"""
Settings check function that reads the settings file under ForinApp/Config/
returns the setting selected in the settings file by reading the file
"""
def settings_check(setting):
	txt = open('Config/Settings.txt', 'r')
	txt_lines = txt.readlines()
	txt.close()	

	for line in txt_lines:
		if line.find(setting) != -1:			#if setting found
			line = line.rstrip('\n')		
			name, statement = line.split(':')	#format string
			break
		else:
			pass

	return statement

"""
settings_index returns the index number for a specfic setting (used with get_settings)
"""
def settings_index(setting):
	txt = open('Config/Settings.txt','r')
	txt_lines = txt.readlines()
	txt.close()

	for count, line in enumerate(txt_lines):
		if line.find(setting) != -1:
			index = count
			break
	return count

"""
get_settings function that returns a list of txt file lines
"""
def get_settings_txt():
	txt = open('Config/Settings.txt','r')
	txt_lines = txt.readlines()
	txt.close()
	return txt_lines

"""
get_settings_list gets all options from options.txt
returns a list of setting.classes
"""
def get_settings_list():
	txt = open('Config/Settings.txt','r')
	txt_lines = txt.readlines()
	txt.close()

	section = ''
	description = ''
	items = ''
	code = ''
	settings_list = []

	check = 0
	for count, line in enumerate(txt_lines):	#read line and store
		if line.startswith('@@') == True:
			continue
		if line.find('-----') != -1:
			section = line.strip()
		elif line.find('#') != -1:
			description = line.strip()
			check = check + 1
		elif line.find('[') != -1:
			items = line.strip()
			check = check + 1
		elif line.find('$') != -1:
			code = line.strip()
			check = check + 1
		if check == 3:				#when filled, append to list
			check = 0
			settings_list.append(Setting(section, description, items, code))

	return settings_list

"""
settings_update updates the settings.txt file
requires a list of lines (get_settings_txt())
"""
def settings_update(setting_txt):
	txt = open('Config/Settings.txt','w')
	for line in setting_txt:
		txt.write(line)
	txt.close()
	
