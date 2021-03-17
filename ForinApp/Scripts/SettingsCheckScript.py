import sys
import os

"""
Settings check function that reads the settings file under ForinApp/Config/
returns the setting selected in the settings file by reading the file
"""
def settings_check(setting):
	txt = open('Config/Settings.txt', 'r')
	txt_lines = txt.readlines()	

	for line in txt_lines:
		if line.find(setting) != -1:
			line = line.rstrip('\n')
			name, statement = line.split(':')
			break
		else:
			pass

	txt.close()
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
get_settings function that returns a list of file lines
"""
def get_settings():
	txt = open('Config/Settings.txt','r')
	txt_lines = txt.readlines()
	txt.close()
	return txt_lines
























	
