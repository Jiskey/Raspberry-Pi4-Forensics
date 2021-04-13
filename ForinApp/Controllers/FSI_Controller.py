#Python FSI_Controller (File System Inspection)
#Application Name: Forin
#Author: J.Male
#Desc: 
#	Handles all of the operations within the application realting to File System Inspection And The Sleuth Kit.

import click
import sys
import os
import time

from View import MainMenu_Controller
from Model.FsiSetting import FsiSetting
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms
from Scripts import UsageLoggingScript as uls

"""
FSI Controller Main Menu
Requests The User To Select A IMG File For Inspection
Can Take A Path Specified When Being Called To Save New Chosen Dir
"""
def FSI_main_menu(*path):
	ext_list = set({})
	choices = []
	title = ''	

	if path:
		path = str(path[0])
		if path == '0':
			path = scs.settings_check('$Default_Output_Location')
	else:
		path = scs.settings_check('$Default_Output_Location')

	os.system('clear')
	click.secho('File System Inspection (Sleuth Kit)\n', bold=True, fg='blue')
	click.echo('File System Inspection Of A Forensic Img File Using TSK [MMLS, FLS, IMG_STAT, ICAT, ISTAT, FSSTAT]\n')
	click.echo('Image File Can Be Of The Following Formats:')
	os.system('mmls -i list')
	click.echo('\nCurrent Image Evidance Location: {}'.format(path))
	
	### Get Combatible Img File Formats
	os.system('mmls -i list 2> Config/tmp.txt')
	for count, line in enumerate(open('Config/tmp.txt')):
		if count > 0:
			tmp = line.split()
			ext = tmp[0].strip()
			ext_list.add('.' + ext)
	os.system('rm Config/tmp.txt')
	ext_list.add('.dd')

	if path.endswith('/') != True:
		path += '/'
	for file in os.listdir(path):
		for ext in ext_list:
			if file.endswith(ext) == True:
				choices.append(file)
				continue
	choices.append('[1] -- Select New Evidance Location')
	choices.append('[0] Main Menu')
	title = '\nPlease Select A File To Insepct'

	index_selection = tms.generate_menu(title, choices)		### Selection

	if index_selection == len(choices) - 1:
		MainMenu_Controller.main_menu()
	elif index_selection == len(choices) - 2:
		new_path = tms.generate_string_menu('Evidance File Path', 1)
		FSI_main_menu(new_path)
	else:
		uls_filepath = scs.settings_check('$Default_UsageLog_Location')
		if uls_filepath.endswith('/') == False:
			uls_filepath += '/'
		uls_filepath += 'Fsi_Usage_Logs.txt'
		sel_file = path + choices[index_selection]
		uls.log_change(uls_filepath, 'File_System_Inspection', sel_file)
		FSI_selection(sel_file)

	MainMenu_Controller.main_menu()

"""
FSI_Selection Page
FSI Selection Page is a Page That Requests The User To Either Select A Offset Or View The File System
Executes TSK Tool Commands To Gather Information And Display It To The User
Uses 'img_conf' Of Class.Type(FsiSetting) To Store Needed Information For Extraction & Navigation
Requires a File Path For The Img File To Inspect From 'FSI_main_menu'
"""

def FSI_selection(file_path):
	img_format = ''
	img_FS_format = ''
	fsstat_txt = []
	mmls_txt = []
	fls_txt = []
	choices = []

	file_details = file_path.split('/')
	name, ext = file_details[len(file_details) - 1].split('.')

	fsi_path = scs.settings_check('$Default_FSI_Output')
	if fsi_path.endswith('/') == False:
		fsi_path += '/'
	output_path = fsi_path + name + '/'
	os.system('sudo mkdir ' + output_path)

	os.system('clear')
	click.secho('File System Inspection (Sleuth Kit)\n', bold=True, fg='blue')

	### Create Img_Conf Class
	os.system('img_stat -t ' + file_path + ' > Config/tmp.txt')
	for line in open('Config/tmp.txt'):
		img_format = line.strip()
	os.system('fsstat -t -i ' + img_format + ' ' + file_path + ' > Config/tmp.txt')
	for line in open('Config/tmp.txt'):
		img_FS_format = line.strip()

	img_conf = FsiSetting(name, ext, file_path, img_format, img_FS_format, output_path)

	if img_FS_format == '':
		click.echo('\nSorry Somthing Went Wrong When Processing Your image File')
		click.echo('Please Choose A different File')
		x = input('Press [Enter To Return]')
		FSI_main_menu()

	### Generate Info For Class (Tool Output Information) & Display
	img_conf.gen_fsstat(fsi_path)
	img_conf.gen_fls(fsi_path)
	img_conf.update_fls(0)

	for line in img_conf.get_fsstat_txt():
		click.echo(line)
		
	choices = ['[1] View Files', '[0] Back']
	title = 'What Would You Like To do?'
	
	index_selection = tms.generate_menu(title, choices)		### Selection

	if index_selection == 0:
		FSI_display(img_conf)
	else:
		FSI_main_menu()

"""
FSI Display Page
Displays To The User a List Of Selections Based On The 'fls' Tool Output
Follows The File Structure And Will Enter Directories, Saving The Dir inodes ('nums') To Navigate Back
If The User Selects a File, Then They Will Be Take To 'FSI_export'
Requires a img_conf class from 'FSI_selection'
"""
def FSI_display(img_conf):
	fls_list = img_conf.get_fls_list()
	nav_list = img_conf.get_inode_nav_list()
	choices = []
	title = ''
	nav_str = '/'
	sel_inode = 0

	os.system('clear')
	click.secho('File System Inspection (Sleuth Kit)\n', bold=True, fg='blue')

	click.echo('Using fls to View Files & Directories')
	click.echo('-:Unkown, r:RegulerFile, d:Dir, v:TSK Virtual File (Ignore)\n')

	### Get And Show Files & dir's For Selection
	for nav in nav_list:
		nav_str += str(nav) + '/' 

	choices = ['[1] .', '[2] ..']
	for fls in fls_list:
		choices.append(fls['deleted'] + ' ' + fls['type'] + ' ' + str(fls['inode']) + ' ' + fls['name'])
	title = 'This Is What "fls" Found: {}'.format(nav_str)
	choices.append('[0] Quit')

	index_selection = tms.generate_menu(title, choices)		### Selection

	### Navigation
	if index_selection == len(choices) - 1:
		FSI_selection(img_conf.get_file_path())
	elif index_selection == 1:
		if len(nav_list) < 2:
			if len(nav_list) == 1:
				img_conf.del_inode_nav(0)
			img_conf.update_fls(0)
			FSI_display(img_conf)
		else:
			try:
				last_inode = nav_list[len(nav_list) -2]
				img_conf.del_inode_nav(len(img_conf.get_inode_nav_list()) -1)
				img_conf.update_fls(last_inode)
				FSI_display(img_conf)
			except:
				FSI_selection(img_conf.get_file_path())
	elif index_selection == 0:
		img_conf.update_fls(0)
		FSI_display(img_conf)

	### Detect fls Selection
	elif choices[index_selection].lower().find('v/') != -1:
		FSI_display(img_conf)
		
	elif choices[index_selection].lower().find('d/') != -1:
		if choices[index_selection].split()[0] == '*':
			sel_inode = int(choices[index_selection].split()[2])
		else:
			sel_inode = int(choices[index_selection].split()[1])
		img_conf.update_fls(sel_inode)
		img_conf.add_inode_nav(sel_inode)
		FSI_display(img_conf)

	elif choices[index_selection].lower().find('r/') != -1 or choices[index_selection].lower().find('-/') != -1 or choices[index_selection].lower().find('b/') != -1 or choices[index_selection].lower().find('c/') != -1:
		if choices[index_selection].startswith('*'):
			sel_inode = int(choices[index_selection].split()[2])
		else:
			sel_inode = int(choices[index_selection].split()[1])
		img_conf.set_sel_inode(sel_inode)
		FSI_export(img_conf, index_selection)

"""
FSI Export Page
Displays To The User The Contents Of a Given File (Inode)
User Options Incl. Exporting Files Based on istat (Details), icat (Hex), & The Ability to Extract img Files
Requires a Img_Conf Class & A index_Selection (fls line)
"""
def FSI_export(img_conf, index_selection):
	img_check = False
	sel_fls = img_conf.get_fls(index_selection - 2)
	file_name = ''
	title = '\nWhat Would You Like To Export'
	choices = ['[1] Export Details (istat)', '[2] Export icat Hexdump (icat)', '[3] Export Copy (icat *Mainly jpg/png files)', '[0] back']

	### Check File Selected
	try:
		file_name, file_ext = sel_fls['name'].split('.', -1)
		if file_ext == 'jpg' or 'png' or 'tif' or 'tiff' or 'raw':
			img_check = True
		else:
			file_name = sel_fls['name']
	except:
		file_name = sel_fls['name']

	os.system('clear')
	click.secho('File System Inspection (Sleuth Kit)\n', bold=True, fg='blue')
	click.echo('Using istat to View File Contents\n')
	
	### Display Inode Details
	os.system('istat -r -i ' + img_conf.get_img_format() + ' -f ' + img_conf.get_img_FS_format() + ' ' + img_conf.get_file_path() + ' ' + str(img_conf.get_sel_inode()))
	click.echo('')
	os.system('icat -i ' + img_conf.get_img_format() + ' -f ' + img_conf.get_img_FS_format() + ' ' + img_conf.get_file_path() + ' ' + str(img_conf.get_sel_inode()) + ' | hexdump | head')
	
	index_selection = tms.generate_menu(title, choices)		### Selection
	
	### Export File
	if index_selection == 0:
		click.echo('\nExporting...')
		img_conf.export_istat()
	elif index_selection == 1:
		click.echo('\nExporting...')
		img_conf.export_icat_hex()
	elif index_selection == 2:
		if img_check == True:
			img_conf.export_icat_img(file_ext)
			click.echo('\nExporting...')
		else:
			click.echo('Error: File Not Accepted')
	elif index_selection == 3:
		FSI_display(img_conf)

	time.sleep(1)
	FSI_export(img_conf, index_selection)
	
