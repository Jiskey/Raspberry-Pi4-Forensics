#Python Settings Check Script
#Application Name: Forin
#Author: J.Male
#Desc: 
#	used whenever the app requires data about the application settings
#	Handles I/O Of the Config/settings.txt file

import sys
import os
import time

from Model.Setting import Setting
from View import MainMenu_Controller

"""
Settings check function that reads the settings file under ForinApp/Config/
returns the setting selected in the settings file by reading the file
"""
def settings_check(setting):
	try:
		txt = open('Config/Settings.txt', 'r')
		txt_lines = txt.readlines()
		txt.close()

		for line in txt_lines:
			if line.find(setting) != -1:
				line = line.rstrip('\n')		
				name, statement = line.split(':')
				break
			else:
				pass

		return statement
	except:
		print('Error Reading Config/Settings.txt File! ERROR: ' + setting + '. Returning To Main Menu')
		time.sleep(3)
		MainMenu_Controller.main_menu()
		sys.exit(0)

"""
settings_index returns the index number for a specfic setting (used with get_settings)
"""
def settings_index(setting):
	try:
		txt = open('Config/Settings.txt','r')
		txt_lines = txt.readlines()
		txt.close()

		for count, line in enumerate(txt_lines):
			if line.find(setting) != -1:
				index = count
				break
		return count
	except:
		print('Error Reading Config/Settings.txt File! ERROR: ' + setting + '. Returning To Main Menu')
		time.sleep(3)
		MainMenu_Controller.main_menu()
		sys.exit(0)

"""
get_settings function that returns a list of txt file lines
"""
def get_settings_txt():
	try:
		txt = open('Config/Settings.txt','r')
		txt_lines = txt.readlines()
		txt.close()
		return txt_lines
	except:
		print('Cannot Open Config/Settings.txt File. Returning To Main Menu')
		time.sleep(3)
		MainMenu_Controller.main_menu()
		sys.exit(0)

"""
get_settings_list gets all options from options.txt
returns a list of setting.classes
"""
def get_settings_list():
	try:
		txt = open('Config/Settings.txt','r')
		txt_lines = txt.readlines()
		txt.close()

		section = ''
		description = ''
		items = ''
		code = ''
		settings_list = []

		check = 0
		for count, line in enumerate(txt_lines):
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
			if check == 3:
				check = 0
				settings_list.append(Setting(section, description, items, code))

		return settings_list
	except:
		print('Error Reading Config/Settings.txt File! ERROR: Failed To Generate Settings List. Returning To Main Menu')
		time.sleep(3)		
		MainMenu_Controller.main_menu()
		sys.exit(0)

"""
settings_update updates the settings.txt file
requires a list of lines (get_settings_txt())
"""
def settings_update(setting_txt):
	try:
		txt = open('Config/Settings.txt','w')
		for line in setting_txt:
			txt.write(line)
		txt.close()
	except:
		print('Cannot Open Config/Settings.txt File. ERROR: Failed To Locate File. Returning To Main Menu')
		time.sleep(3)
		MainMenu_Controller.main_menu()
		sys.exit(0)
	
