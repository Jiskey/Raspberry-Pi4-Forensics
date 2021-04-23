#Python DC_Controller (Data Carving)
#Application Name: Forin
#Author: J.Male
#Desc: 
#	Python DC Controller, Handles All Operations With tools Relating To Data Carving
#	Uses The DcObject Class To Store Extension Data Used In [tool].conf files

import click
import sys
import os

from View import MainMenu_Controller
from Model.DcObject import DcObject
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms
from Scripts import DcSettingsScript as dcss
from Scripts import FdiskScript as fds
from Scripts import UsageLoggingScript as uls

"""
DC_main_menu.
Requests a User To Select A Tool, Eaither Foremost, Photorec or Scalple
NOTE: AS OF KALI V2021.1 For The Pi4. SCALPLE DOES NOT FUNCTION WITHOUT TROUBLESHOOTING
"""
def DC_main_menu():	
	choices = ['[1] Foremost (.dd/ .img/ .RAW)','[2] Scalpel (*/ Files/ Connected Drives)','[3] PhotoRec (Indipendent Program)','[4] Main Menu']
	title = '\nPlease Select A Tool'

	### Tool Selection
	os.system('clear')
	click.secho('Data Carving: Scalpel Type\n', fg='blue', bold=True)
	click.echo('There are mutiple tools to perform data_carving. that perform different functions')
	click.secho('*AS OF KALI V2020.4 For The Pi4. SCALPLE DOES NOT FUNCTION WITHOUT TROUBLESHOOTING\n', fg='red', bold=True)
	click.echo('If The User Wishes To Troubleshoot Themsleves, Then Scalple Will Proceed To Function Correctly')

	index_selection = tms.generate_menu(title, choices)

	if index_selection == 0:
		DC_selection('foremost')
	elif index_selection == 1:
		DC_selection('scalpel')
	elif index_selection == 2:
		DC_photorec_selection()
	elif index_selection == 3:
		MainMenu_Controller.main_menu()

	MainMenu_Controller.main_menu()
	
	
"""
DC_Selection, Selection asks the user to select a Drive or Img File For Carving.
Drive Carving Is Only Avalible For Scalpel Thus, Formost Always Returns To 1
Generates Data Required For The DC_conform Function
Requires a Tool Code
"""
def DC_selection(tool):
	conf_path = scs.settings_check('$Foremost_ConfFile_Location')
	choices = []
	path = ''	

	os.system('clear')
	click.secho('Data Carving: Scalpel Type', fg='blue', bold=True)

	### Select What To Carve
	if tool == 'scalpel':
		conf_path = scs.settings_check('$Scalpel_ConfFile_Location')		
		title = '\nWhat Would You Like To Carve?'
		choices = ['[1] Connected Drive','[2] Acquired Img File','[0] Back']
		index_selection = tms.generate_menu(title, choices)
	else:
		index_selection = 1

	### Gather Data Via Path Or Drive
	if index_selection == 0:
		drive_path = DC_selection_drive(path, tool)				
		selected_objs_list = DC_config(conf_path)
		dir_name = DC_selection_dir()					
		DC_conform(selected_objs_list, conf_path, dir_name, tool, drive_path)
	elif index_selection == 1:
		img_path = DC_selection_image(tool)				
		selected_objs_list = DC_config(conf_path)				
		dir_name = DC_selection_dir()
		DC_conform(selected_objs_list, conf_path, dir_name, tool, img_path)
	elif index_selection == 2:
		DC_main_menu()
	else:
		DC_main_menu()

"""
Configuration Menu For Data Carving. 
Generates a list(class(DcObject)) Based On User Selections Via One Of The Wizards
Requires The Conf Filepath For Either Foremost or Scalpel
Returns a Altered List(class(DcObject)) Containg ext Information With Enable/Disable Code (@/#) 
"""
def DC_config(conf_path):
	objs_list = dcss.get_DC_settings_list(conf_path)
	title = '\nHow Would You Like To Proceed?'
	choices = ['[1] Use Currently Selected Options','[2] Simple Wizard (Type based)','[3] Advanced Wizard (Individual Files)', '[0] Back']	

	os.system('clear')
	click.secho('Data Carving: Config', fg='blue', bold=True)
	click.echo('\nThis will edit and select Different File Types in the .conf file')
	click.echo('Conf file found under: ' + conf_path)
	click.echo('If You Are unsure What This Means, Please Refer to The file Above For More Information')
	click.echo('\nCurrently Saved Options Under Catergories:')

	### Currently Saved .Conf File Options
	for obj in objs_list:
		check = 0
		for ext in obj.get_exts():
			if ext[0] == '@' and check == 0:
				click.echo(obj.get_cat().strip())	
				check = check + 1

	index_selection = tms.generate_menu(title, choices)

	### Generate Objs List based On input
	if index_selection == 0:
		return objs_list
	elif index_selection == 1 or index_selection == 2:
		for obj in objs_list:
			for ext in obj.get_exts():
				ext[0] = '#'
		new_objs_list = DC_Wizard(index_selection, objs_list, conf_path)
		return new_objs_list
	elif index_selection == 3:
		DC_main_menu()

	MainMenu_Controller.main_menu()

"""
DC Conformation Page.
Displays All Settings & Actions To The User Aswell as The Command Generated.
Contains a Warning Prompt With A 2 Second Freeze Time
Requires A Objs_List, .Conf Filepath, Output Dir Name, Tool Name, Img/Drive Path
"""
def DC_conform(selected_objs_list, conf_path, dir_name, tool, img_path):	
	check = 0
	files = ''
	all_files = ''
	title = '\nYou Are About To Execute The Above Command Do You With To Proceed?'
	uls_filepath = scs.settings_check('$Default_UsageLog_Location')
	old_txt = list(dcss.get_DC_settings_txt(conf_path))
	new_txt = old_txt

	command = 'sudo {} '.format(tool)
	if tool == 'foremost':
		command += '-T -v -c {} {} -o {}/'.format(conf_path, img_path, dir_name)
	if tool == 'scalpel':
		command += '-v -c {} {} -o {}/'.format(conf_path, img_path, dir_name)

	### Display Selected File Ext's
	os.system('clear')
	click.secho('Data Carving: Conform\n', fg='blue', bold=True)
	click.secho('Selected Data Carving Tool: ', bold=True)
	click.echo(tool)
	click.secho('Selected Drive/File To Carve: ', bold=True)
	click.echo(img_path)
	click.secho('Selected Output Location:', bold=True)
	click.echo('ForinApp/')
	click.secho('Selected Output Dir Name:\n', bold=True)
	click.echo(scs.settings_check('$DC_Output_Location_Name'))

	if len(selected_objs_list) <= 1:
		obj = selected_objs_list
		print(obj)

	for count, obj in enumerate(selected_objs_list):
		if files != '':
			click.echo(files.strip())
		files = ''
		check = count
		for ext in obj.get_exts():
			if ext[0] == '@' and check == count:
				check = check + 1
				click.secho(obj.get_cat().strip(), bold=True)
			if ext[0] == '@':
				files += ext[1] + ', '
				all_files += ext[1] + ', '
	else:
		if files != '':
			click.echo(files.strip())		

	click.secho('\n- --- - WARNING - --- - --- - WARNING - --- - --- - WARNING - --- -', fg='red', bold=True)
	click.secho('Changes will be made to the scalpel.conf file', bold = True)
	click.secho('\nCOMMAND:', bold=True)
	click.echo(command)

	index_selection = tms.generate_promt_menu(title, 2)

	### Generate New Txt And Edit, Execute Then Revert The .Conf File
	if index_selection == 0:
		DC_main_menu()
	elif index_selection == 1:
		if uls_filepath.endswith('/') == False:
			uls_filepath += '/'
		uls_filepath += 'Dc_Usage_Logs.txt'
		uls.log_change(uls_filepath, 'Data_Carve_Attempt', ((command + '\n'), (all_files + '\n\n')))
		new_txt = dcss.create_DC_settings_txt(new_txt, selected_objs_list)
		dcss.set_DC_settings_txt(new_txt, conf_path)
		os.system('clear')
		os.system(command)
		#dcss.set_DC_settings_txt(old_txt, conf_path)
		wait_selection = tms.generate_menu('\nOperation Complete. Please Press Enter To Continue: ENTER', [' '])

	MainMenu_Controller.main_menu()

"""
DC Wizards, Contains 2 Wizards That Display Dc Objects Either By Categories Or File.ext.
Uses Script So Generate A Multi_Select Simple_Term_Menu That Returns A List(str(selections))
Requires a Menu_Selection Check, a list(DcObjects) And a Conf File Path
Returns a Altered list(DcObjects)
"""
def DC_Wizard(menu_selection, objs_list, conf_path):
	type_choices = ['[1] Select All']	
	file_choices = ['[1] Select All']
	check = ''
	
	os.system('clear')
	click.secho('Data Carving: File Type Selection', fg='blue', bold=True)
	click.echo('\nIf custom options are added to the .conf file, they will be detected')

	### Generate Choices (Either Category Or Ext)		
	for obj in objs_list:
		type_choices.append(obj.get_cat().strip())
		for count, ext in enumerate(obj.get_exts()):
			file_choices.append(ext[1].strip() + '  ' + ext[3].strip() + '  ' + ext[4].strip())
	type_choices.append('[0] Back')
	file_choices.append('[0] Back')	

	if menu_selection == 1:								
		title = '\nPlease Select the Type Of Files You Wish to Carve'	
		title += '\nSelect "Select All" to select everything on exit or select "Back" to leave on exit\n'
		index_selection = tms.gernerate_multi_select_menu(title, type_choices, True)	
		check = 'simp'
	elif menu_selection == 2:								
		title = '\nPlease Select the Files You Wish to Carve'
		title += '\nSelect "Select All" to select everything on exit or select "Back" to leave on exit\n'
		title += '\n     Ext   Size   Header/Footer'
		index_selection = tms.gernerate_multi_select_menu(title, file_choices, True)
		check = 'adv'
	else:
		MainMenu_Controller.main_menu()
	
	### Generate New List Based On Selections
	new_objs_list = dcss.set_DC_settings_list(objs_list, index_selection, check)

	if type(new_objs_list) != list:
		DC_config(conf_path)

	return new_objs_list

"""
Directory Selection Page, Asks a User To select A Path Name For The Carved Evidance.
Can Select Either A Saved Default Name Or Specify A New Name (Carved Data is Taged With Time So Name Can == Anything)
Returns a Directory Path Name For The Carved Evidance
"""
def DC_selection_dir():
	title = '\nPlease Select The Name Of The Directory Where The Evidence Will Be Stored:'
	settings_list = scs.get_settings_list()
	name = scs.settings_check('$DC_Output_Location_Name')	
	choices = []

	os.system('clear')
	click.secho('Data Carving: Dir/Folder Name', fg='blue', bold=True)
	click.echo('\nCurrently Saved Name: {} (will format name if dir already exsists)'.format(name))

	for setting in settings_list:
		if setting.get_code_call() == '$DC_Output_Location_Name':
			for choice in setting.get_items_list():
				choices.append(choice)

	choices.append('[1] Use Default: {}'.format(name))
	choices.append('[0] Back')
	
	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		DC_main_menu()
	elif choices[index_selection].startswith('--') == True:
		name = tms.generate_string_menu(setting.get_code_call() == '$DC_Output_Location_Name', 0)
	else:
		pass	

	return name
	
"""
DC Drive Selection Tool (Scalpel Tool Only).
Uses The fdisk Script Similer To ACQ To Gather Drive Information
Returns a Path of The Selected Drive / Partition
Requires a str (can be empty) And a Tool Code
"""
def DC_selection_drive(drive_path, tool):
	title = 'Please Select a Drive'
	drives = fds.fdisk(False, False)
	choices = []
	check = 1

	os.system('clear')
	click.secho('Data Carving (Scalpel): Drive Selection\n', fg='blue', bold=True)
	click.echo('Scalpel Has The Ability To Carve From Drives Connected To The Device')

	### Get Connected Drives
	for drive in drives:
		if drive.get_boot() == True and scs.settings_check('$Boot_Drive_Override') == 'True':
			choices.append('[{}] {}'.format(check, drive.get_path()))
			check = check + 1
		elif drive.get_boot() == False:
			choices.append('[{}] {}'.format(check, drive.get_path()))
			check = check + 1
	choices.append('[0] Back')

	index_selection = tms.generate_menu(title, choices)

	### Get Partition
	if index_selection == len(choices) - 1:
		DC_main_menu()

	sel_dc_drive = choices[index_selection]
	sel_dc_drive = sel_dc_drive.split()[1]
	for drive in drives:
		if drive.get_path() == sel_dc_drive:
			dc_drive = drive

	choices = ['[1] Full Drive']
	for part in dc_drive.get_partitions():
		choices.append(part.split(':')[0])
	choices.append('[0] Back')

	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		DC_selection(tool)
	elif index_selection == 0:
		sel_drive_path = dc_drive.get_path()
	else:
		sel_drive_path = choices[index_selection]

	return sel_drive_path
	 
"""
DC Image Selection Page, Requires The User To Select A Img File To Carve.
Requires The Tool That Was Selected And a Path Which Is Passed
Returns a Full Path With File_Path + Name
"""
def DC_selection_image(tool, path=scs.settings_check('$Default_Output_Location')):
	choices = []
	title = '\nWhat Would You Like To Carve?\nIf You Dont See Any Files Try Specifying a Custom Path In The Settings'	

	os.system('clear')
	click.secho('Data Carving: Image Selection', fg='blue', bold=True)
	click.echo('Currently Selected Evidance Path: {}'.format(path))

	### Discovery Of Image File Is Saved OutputLocation
	for file in os.listdir(path):
		if file.lower().endswith('.dd') or file.lower().endswith('.img') or file.lower().endswith('.raw') or file.lower().endswith('.aff'):
			choices.append(file)
	choices.append('[1] -- Specify New Evidance Path')
	choices.append('[0] Back')

	index_selection = tms.generate_menu(title, choices)
	
	if index_selection == len(choices) - 1:
		DC_main_menu()
	elif index_selection == len(choices) - 2:
		index_selection = tms.generate_string_menu('Forensic Image File Location:', 1)
		DC_selection_image(tool, index_selection)
	else:
		img_file_name = choices[index_selection]
		return path + str(img_file_name)

	MainMenu_Controller.main_menu()

"""
Photorec Selection Page, Is a Prompt Page Asking The User If They Wish To Procced
"""
def DC_photorec_selection():
	title = '\nWould You Like To Procced ToUse PhotoRec?'
	choices = ['[1] Lauch PhotoRec', '[0] Back']

	os.system('clear')
	click.secho('Data Carving: PhotoRec\n', fg='blue', bold=True)
	click.echo('PhotoRec is a powerful data recovery tool similer to the others in this program')
	click.echo('However, PhotoRec Takes Advanatge of its own Wizard')
	click.secho('\nWARNING: PhotoRec Will Be Run As SU', fg='red')

	index_selection = tms.generate_menu(title, choices)

	if index_selection == 0:
		os.system('sudo photorec')
	else:
		DC_main_menu()
	
	MainMenu_Controller.main_menu()
	
