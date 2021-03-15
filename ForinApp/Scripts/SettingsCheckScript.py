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
