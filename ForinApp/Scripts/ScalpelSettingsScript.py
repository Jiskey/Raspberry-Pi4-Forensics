#Python Scaple Settings Script
#Used whenever the app edits or requires the scalpel conf file (scalpel.conf)

import click
import sys
import os

from Model.ScalpelSetting import ScalpelSetting

"""
get_scalpel_settings_txt gets the scalple config file text.
returns a list of txt_lines.
"""
def get_DC_settings_txt(path):
	check = False
	txt = open(path)
	txt_lines = txt.readlines()
	txt.close()

	return txt_lines

"""
Writes to the scalpel config file.
requires a list(lines).
"""
def set_DC_settings_txt(new_txt, path):
	txt = open(path,'w')			#write to file
	for txt_line in new_txt:	
		txt.write(txt_line)
	txt.close()

"""
get_scalpel_settings_list gets the scalpel config file text and converts them... 
into a list of class(ScalpleSetting) based on the layout of the scalpel.conf file.
setting.get_options(list(option([0 = tag][1 = ext][2 = case_sens][3 = size][4 = extra1]...)).
returns a list with class(ScalpelSetting(cat, options())).
"""
def get_DC_settings_list(path):
	check = False
	txt = open(path)
	txt_lines = txt.readlines()
	txt.close()
	
	cat = ''
	options = []
	
	settings_list = []

	cat_check = False
	for count, line in enumerate(txt_lines):
		if line.startswith('#-----') and cat_check == False and count > 3:		#check for main category
			settings_list.append(ScalpelSetting(cat, options))
			cat = ''
			options = []
			cat = txt_lines[count + 1].strip()
			cat_check = True
		elif cat_check != False:
			if line.startswith('#-----'):
				cat_check = False
				continue
			else:
				continue

		if line.startswith('#\n') == True or line.startswith('# ') == True:				#ignore empty lines
			continue

		try:							# try to split line
			setting_line = line.split()
			if type(int(setting_line[2])) == int:
				setting_line.insert(0, '@')
				options.append(setting_line)
		except:
			pass
		try:							# try to split line
			setting_line = line.split()
			if type(int(setting_line[3])) == int:
				options.append(setting_line)
		except:
			pass
	else:
		settings_list.append(ScalpelSetting(cat, options))	#append last when EOF

	settings_list.pop(0)						#remove starting 'fake'
	settings_list.pop(0)						#remove scalpel example

	return settings_list

"""
takes in a settings_list[x] containing class(ScalpelSetting) and alters...
the options within based on a list of user selections from the multi_select terminal menu.
requires a settings_list, index_selection = list(strings of user selections), wizard_check code
returns an altered settings_list
"""
def set_DC_settings_list(settings_list, index_selection, check):

	select_all = False					#check for select all
	for index in index_selection:				
		if index == 0 or index ==  'Select All':
			select_all = True
		if len(index_selection) == 0 or index == 'Back':
			return 0

	for setting in settings_list:				#for each option in each settings
		if check == 'adv':
			for option in setting.get_options():
				if select_all == True:
					option[0] = '@'			#tag all
				else:
					for index in index_selection:
						header = index.split()
						if option[4].strip() == header[2].strip():
							option[0] ='@'			#tag selected
		else:
			for option in setting.get_options():
				for index in index_selection:
					if index.strip() == setting.get_cat().strip():
						option[0] = '@'

	return settings_list

"""
takes a list of file lines and converts enable/disable setting based on...
the selected_settings_list and matches the scalpel setting.conf format...
requries a list(file lines) and a list(altered: class(ScalpelSetting))
returns a updated list(new_txt)
"""
def create_DC_settings_txt(new_txt, selected_settings_list):
	enable_codes = []						#what files to enable / disable
	disable_codes = []

	for count, line in enumerate(new_txt):
		for setting in selected_settings_list:
			for option in setting.get_options():
				if line.find(str(option[4])) != -1:
					if option[0] == '#':
						if line.startswith('#') == False:		#if set to disabled by selection but enabled in config
							disable_codes.append(count)
					elif option[0] == '@':
						if line.startswith('#') == True:		#if set to enabled by selection but disabled in config
							enable_codes.append(count)

	for code in disable_codes:		#update txt lines to disable
		tmp_txt = ''			#following scalpel.conf format
		temp = new_txt[code].split()
		temp[0].strip()
		if temp[0] != '#':
			temp.insert(0, '#')
		for tmp in temp:
			tmp_txt += tmp + '\t'
		new_txt[code] = tmp_txt + '\n'

	for code in enable_codes:		#update txt lines to enable
		tmp_txt = ''
		temp = new_txt[code].split()
		temp[0].strip()
		temp.pop(0)
		temp.insert(0, ' ')
		for tmp in temp:
			tmp_txt += tmp + '\t'
		new_txt[code] = tmp_txt + '\n'

	return new_txt				#return updated str list

