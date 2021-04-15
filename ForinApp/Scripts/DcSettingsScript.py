#Python DC (Data Carving) Setting Script
#Application Name: Forin
#Author: J.Male
#Desc: 
#	DC Settings Script Is a Script That Handles All Functions Regarding The .Conf File Of Either...
#       Foremost Or Scalpel. Creates And Edits Settings Lists (list of .conf file obj's & .ext's)

import click
import sys
import os

from Model.DcObject import DcObject

"""
Get_DC_Settings_txt Gets The Data Carving Tool Conf File.
Returns a List of Txt File Lines
"""
def get_DC_settings_txt(path):
	check = False
	txt = open(path)
	txt_lines = txt.readlines()
	txt.close()

	return txt_lines

"""
Writes To The Data Carving Tool Config File.
Requires a List(txt_lines).
"""
def set_DC_settings_txt(new_txt, path):
	txt = open(path, 'w')
	for txt_line in new_txt:	
		txt.write(txt_line)
	txt.close()

"""
get_DC_settings_list Gets The Data Carving Tool Config File Text And Converts Them... 
Into a List of Class(DcObejct) Based On The Layout Of The Datacarving Tool Conf File.
DcObject.get_exts(list(ext([0 = tag][1 = ext][2 = case_sens][3 = size][4 = header]...)).
Returns a list With Class(DcObejct(category, list(exts))).
"""
def get_DC_settings_list(conf_path):
	txt = open(conf_path)
	txt_lines = txt.readlines()
	txt.close()
	check = False
	new_cat = ''
	cat = ''
	exts = []
	objs_list = []
	cat_check = False

	### Search .Conf File For Objects && Create List Of DcObjects
	for count, line in enumerate(txt_lines):
		if line.startswith('#-----') and cat_check == False and count > 3:
			objs_list.append(DcObject(new_cat, exts))
			new_cat = ''
			cat = ''
			exts = []
			cat = txt_lines[count + 1].strip()
			cat = cat.split()
			for i in cat:
				new_cat += ' ' + i 
			cat_check = True
		elif cat_check != False:
			if line.startswith('#-----'):
				cat_check = False
				continue
			else:
				continue

		if line.startswith('#\n') == True:
			continue

		### Capture Conf Object by 'Size' type(int) Check
		try:							
			obj_line = line.split()
			if type(int(obj_line[2])) == int:
				if int(obj_line[2]) == 95:		#ignore windows 95 title call >:(
					pass
				else:
					obj_line.insert(0, '@')
					exts.append(obj_line)
		except:
			pass
		try:				
			obj_line = line.split()
			if type(int(obj_line[3])) == int:
				if int(obj_line[3]) == 95:
					pass
				else:
					exts.append(obj_line)
		except:
			pass
	else:
		objs_list.append(DcObject(new_cat, exts))	

	objs_list.pop(0)						
	objs_list.pop(0)						
	return objs_list

"""
set_DC_settings_list Takes a List Containing class(DcObject) & Edits The Objects Within...
Based On a List Of User Selections From Simple_Term_Menu.
Requires a Dc_objs_list, index_selection = list(Strings Of Users Selections), Wizard type check Code
Returns a Altered DcObject List
"""
def set_DC_settings_list(objs_list, index_selection, check):
	select_all = False

	for index in index_selection:				
		if index == 0 or index ==  'Select All':
			select_all = True
		if index == 'Back':
			return 0

	### Read Selections A Set Tag To: @ == Enable / adv = enable by cat
	for obj in objs_list:
		if check == 'adv':
			for ext in obj.get_exts():
				if select_all == True:
					ext[0] = '@'
				else:
					for index in index_selection:
						header = index.split()
						if ext[4].strip() == header[2].strip():
							ext[0] ='@'
		else:
			for ext in obj.get_exts():
				if select_all == True:
					ext[0] = '@'	
				else:
					for index in index_selection:
						if index.strip() == obj.get_cat().strip():
							ext[0] = '@'

	return objs_list

"""
Takes a List of Conf File Lines And Enables/Disables Them Besed On The Passed objs_list
Objs_list(etxs)[0] Are Read (@/#) To Apply A Code To Alter new_txt lines.
Requries a List(.Conf File Lines) And a list(altered: class(DcObject))
Returns A Updated List(new_txt)
"""
def create_DC_settings_txt(new_txt, selected_objs_list):
	enable_codes = []						
	disable_codes = []
	check = 0

	### Read Currently Saved .Conf File Options
	for obj in selected_objs_list:
		for ext in obj.get_exts():
			for count, line in enumerate(new_txt):
				check = 0
				if line.find(str(ext[4])) != -1:
					if ext[0] == '#' and line.startswith('#') == False:		
						new_txt[count + check] = '#\t' + new_txt[count + check].strip() + '\n'
						check = check + 1
					elif ext[0] == '@' and line.startswith('#') == True:		
						new_txt[count + check] = new_txt[count + check][1:]
						check = check + 1
	return new_txt