#Python 
#Application Name: Forin
#Author: J.Male
#Desc: 
#	Handles All Operations In Realation To Password/Hash Cracking (Hashcat)
#	Asks users for Files such as a list of hashses, dictonaries and rule files
#	Contains Custom Mask/Charset Generator For BruteForce/Hybrid Attacks

import click
import sys
import os

from View import MainMenu_Controller
from Model.PwdObject import PwdObject
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms
from Scripts import UsageLoggingScript as uls

"""
Pwd_main_menu acts as the main menu from the program
asks the user to specify a file to crack
can take a new specified path if required.
Send the user through mutiple functions to generated attack
"""
def PWD_main_menu(path = '0'):
	choices = []
	title = ''
	if path and path != '0':
		evi_path = path
		if evi_path.endswith('/') == False:
			evi_path = evi_path + '/'
	else:
		evi_path = scs.settings_check('$Default_Application_Evidance_Search_Location')
		if evi_path.endswith('/') == False:
			evi_path = evi_path + '/'

	os.system('clear')
	click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')
	click.secho('Crack Hashes And Passwords With Use Of Mutliple Different Attack Methods', bold=True)
	click.echo('Hashcat Is A Powerful Hash Cracking Tool With Many Options To Assist In This Demanding Task')
	click.echo('Password Cracking Is A very Demanding Task and Requires Powerful GPUs To Perform! Expect System Slowdown')	
	click.echo('\nCurrent Image Evidance Location: {}\n'.format(evi_path))

	### Select File To Crack
	title = 'Please Select A File That Contains The Hash Lines To Crack:'
	try:
		for file in os.listdir(evi_path):
			if os.path.isfile(evi_path + str(file)) == True and str(file).startswith('.') == False:
				choices.append(file)
	except:
		click.secho('Error Loading Directory! Check Settings File OR specify A New Dir!\n', fg='red')

	choices.append('[1] -- Specify Hash File Evidance Directory')
	choices.append('[0] Back')
	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		MainMenu_Controller.main_menu()
	elif index_selection == len(choices) - 2:
		index_selection = tms.generate_dir_menu()
		if index_selection == '0':
			PWD_main_menu()
		else:
			PWD_main_menu(index_selection)
	
	### Create Pwd_Object and set options
	pwd_object = PwdObject(evi_path, choices[index_selection])

	PWD_hash_type(pwd_object)
	PWD_attack_type(pwd_object)
	PWD_config(pwd_object)
	PWD_conform(pwd_object)

"""
Pwd_hash_type asks the user for the type of hash they wish to crack.
If list is selected, PWD_hash_type_wizard is called
Requires a PWD_object that contains details about the attack
"""
def PWD_hash_type(pwd_object):
	choices = ['0 - MD5', '100 - SHA1', '1400 - SHA2-256', '1700 - SHA2-512', '1000 - NTLM' ,'[1] Select From List', '[0] back']
	title = '\nPlease Select The hash Type Of The Has You wish To Crack'	

	os.system('clear')
	click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')
	click.secho('There Are Many Hashes That Can Be Used!', bold=True)
	click.echo('You Must Know The Hash Type Before Attmepting To Crack It')
	click.echo('Its Hard To Tell Which Hashes Are What Sometimes. Some do Have Identifers!')
	click.echo('MD5 Hash Example; baade50c0278b90b546974280789201a;')
	click.echo('Common Hashes Are Below, Or Veiw The List For All Hashcat Support Hashes.')

	### Select hash type
	index_selection = tms.generate_menu(title, choices)

	if index_selection == 6:
		PWD_main_menu(pwd_object.get_filepath())
	elif index_selection == 5:
		PWD_hash_type_wizard(pwd_object)
	else:
		pwd_object.set_pass_hash(int(choices[index_selection].split()[0]))

"""
Pwd_attack_type asks the user what type of attack they with to use
sends user to wizards to create information needed for chosen attack
requires pwd_object
"""
def PWD_attack_type(pwd_object):
	title = '\nWhat Type Of Attack Would You Like To Take?'
	choices = ['[1] Dictonary','[2] Rules Based','[3] Combinator','[4] Brute Force','[5] Hybrid','[0] Back']

	os.system('clear')
	click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')
	click.secho('Different Attack Types Require Diffrerent Inputs/Files', bold=True)
	click.echo('1. Dictonary Attack = Standard Dictonary Based Attack (Dict File)')
	click.echo('2. Rules Based Attack = Standard Dictonary Based Attack With A Set Of Rules (Dict File + Rule File)')
	click.echo('3. Combinator Attack = Standard Dictonary Based Attack With Multiple Dicts (Concatination) (Dict File x2)')
	click.echo('4. Brute Force + Mask Attack = Brute Force Attack With The Use Of A Generated Mask (Created Mask)')
	click.echo('5. Hybrid = Dictonary + Mask Attack OR Mask + Dictonary Attack (Created Mask + Dict File)')

	### Select Attack Type To Use
	index_selection = tms.generate_menu(title, choices)

	if index_selection == 5:
		pwd_object.set_sel_rule('')
		PWD_main_menu(pwd_object.get_filepath())
	elif index_selection == 4:
		pwd_object.set_sel_rule('')
		choices = ['[1] Mask:Dict','[2] Dict:Mask']
		title = '\nPlease Select A Format'
		index_selection = tms.generate_menu(title, choices)
		if index_selection == 0:
			pwd_object.set_attack(7)
		elif index_selection == 1:
			pwd_object.set_attack(6)
		PWD_sel_dict(pwd_object)
		PWD_gen_mask(pwd_object)
	elif index_selection == 3:
		pwd_object.set_attack(3)
		pwd_object.set_sel_rule('')
		PWD_gen_mask(pwd_object)
	elif index_selection == 2:
		pwd_object.set_attack(1)
		pwd_object.set_sel_rule('')
		PWD_sel_dict(pwd_object)
	elif index_selection == 1:
		pwd_object.set_attack(2)
		PWD_sel_dict(pwd_object)
	elif index_selection == 0:
		pwd_object.set_sel_rule('')
		pwd_object.set_attack(0)
		PWD_sel_dict(pwd_object)

"""
Pwd_config asks the user what type of configuration options they would like
checks the Config/settings.txt file for saved settings and sets to pwd_object
"""
def PWD_config(pwd_object):
	pwd_object.set_workload(scs.settings_check('$Default_Workload_Profile'))
	pwd_object.set_optimised_kernal(scs.settings_check('$Optimised_Kernal'))
	pwd_object.set_output_path(scs.settings_check('$Default_PWD_Output'))
	pwd_object.set_max_runtime(int(scs.settings_check('$Max_Runtime')))
	pwd_object.set_potfile(scs.settings_check('$Enable_Hashcat_Potfile'))
	title = '\nPlease Select An Option:'
	choices = ['[2] Specify New Options', '[1] Use Default', '[0] Back']

	os.system('clear')
	click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')
	click.echo('Currently Selected Configuration Options:\n')
	click.echo('WorkLoad Performace: {}'.format(str(pwd_object.get_workload())))
	click.echo('Hashcat Optimised kernal: {}'.format(str(pwd_object.get_optimised_kernal())))
	click.echo('Max Operation Runtime: {}'.format(str(pwd_object.get_max_runtime())))
	click.echo('Enable Hashcat Potfile: {}'.format(str(pwd_object.get_potfile())))
	click.echo('Default Output Location: {}'.format(str(pwd_object.get_output_path())))

	### Select Config Options To Use
	index_selection = tms.generate_menu(title, choices)

	if index_selection == 2:
		PWD_attack_type(pwd_object)
		PWD_config(pwd_object)
	elif index_selection == 0:
		PWD_config_wizard(pwd_object)

"""
PWd_conform is the conformation page to execute hashcat
contains a warning for headless mode, a prompt, and updates usage logs
returns to main_menu of application after hashcat operation
"""
def PWD_conform(pwd_object):
	title = '\n'
	if pwd_object.get_workload() == 4:
		title = title + '\nWARNING! HEADLESS WORKLOAD DETECTED. EXPECT HUGE PERFORMANCE HIT!\n'
	title = title + 'You Are About To Execute The Following Command!'

	os.system('clear')
	click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')
	click.secho('Target Information:', bold=True)
	click.echo('To Crack: {}'.format(pwd_object.get_filepath() + pwd_object.get_filename()))
	click.echo('Output Path: {}'.format(pwd_object.get_output_path()))

	### Print Selected Settings based On Attack Type
	if pwd_object.get_attack() == 0:
		click.secho('\nAttack Type: Strait', bold=True)
		click.echo('Dictonary File: {}'.format(pwd_object.get_dict_file(0)))
		click.echo('Rule File: {}'.format(pwd_object.get_sel_rule()))
	elif pwd_object.get_attack() == 1:
		click.secho('\nAttack Type: Combinator', bold=True)
		click.echo('Dictonary File: {}'.format(pwd_object.get_dict_file(0)))
		click.echo('Secondary Dictonary File: {}'.format(pwd_object.get_dict_file(1)))
	elif pwd_object.get_attack() == 3:
		click.secho('\nAttack Type: Brute-Force (Mask) Attack', bold=True)
		for charset in pwd_object.get_custom_charset_list():
			click.echo('Custom Charset 1: ' + charset)
		click.echo('Cracking Mask: {}'.format(pwd_object.get_pass_mask()))
	elif pwd_object.get_attack() == 6 or pwd_object.get_attack() == 7:
		if pwd_object.get_attack() == 6:
			hybrid_format = 'Dictonary + Mask'
		else:
			hybrid_format = 'Mask + Dictonary'
		click.secho('\nAttack Type: Hybrid Attack', bold=True)
		click.echo('Hybrid Format: ' + hybrid_format)
		click.echo('Dictonary File: {}'.format(pwd_object.get_dict_file(0)))
		click.echo('Cracking Mask: {}'.format(pwd_object.get_pass_mask()))

	click.secho('\nConfiguration Options', bold = True)
	click.echo('Workload: {}'.format(pwd_object.get_workload()))
	click.echo('Optimised Kernal: {}'.format(pwd_object.get_optimised_kernal()))
	click.echo('Max Program Runtime: {}'.format(pwd_object.get_max_runtime()))

	### generate & Execute Command
	command = pwd_object.gen_command()
	click.secho('\n- --- - WARNING - --- - --- - WARNING - --- - --- - WARNING - --- -', fg='red', bold=True)
	click.secho('\nCOMMAND:', bold=True)
	click.echo(command)

	index_selection = tms.generate_promt_menu(title, 2)

	if index_selection == 0:
		PWD_config(pwd_object)
		PWD_conform(pwd_object)
	else:
		logfile = scs.settings_check('$Default_UsageLog_Location')
		if logfile.endswith('/') == False:
			logfile += '/'
		logfile += 'Pwd_Usage_Logs.txt'
		uls.log_change(logfile, 'Password_Crack_Attempt', command + '\n')	
		os.system('clear')
		os.system(command)			### EXECUTE
		index_selection = tms.generate_menu('\n Please Press Any Button To Contnue', ' ')
		MainMenu_Controller.main_menu()
		

"""
pwd_hash_type_wiazrd is a page that checks the full list of hashes to use with hashcat
uses hashcat --help to print output and collect relevent hash types and display to the user
sets the hash type of the pwd_object
"""
def PWD_hash_type_wizard(pwd_object):
	choices = []	
	title = 'Please Select The hash Type Of The Has You wish To Crack From The List'
	tmp_txt = ''	

	### Generate All Hashes From hashcat --help command
	pwd_object.gen_hash_list()
	
	for hash_item in pwd_object.get_hash_list():
		tmp_txt = ''
		split_item = hash_item.split()
		for count, item in enumerate(split_item):
			if count == 0:
				length = len(item)
				for x in range(8 - length):
					item = item + ' '
				tmp_txt = tmp_txt + ' ' + item
			elif item == '|':
				item = '---'
				tmp_txt = tmp_txt + ' ' + item
			else:
				tmp_txt = tmp_txt + ' ' + item.strip()
					
		choices.append(tmp_txt)
	choices.append('[0] Back')

	### User Select Hash From list
	index_selection = tms.generate_menu(title, choices)
	
	if index_selection == len(choices) - 1:
		PWD_hash_type(pwd_object)
	else:	
		pwd_object.set_pass_hash(int(choices[index_selection].split()[0]))


"""
pwd_sel_dict is the function that lets the user select a dictonary file for the attack
also allows user to select either a rule file or another dictonary based on attack code
sets the dictonaries and rules for the attack type on pwd_object
"""
def PWD_sel_dict(pwd_object, path = '0'):
	pwd_object.set_dict_list([])
	choices = []
	title = ''

	if path == '0':
		path = pwd_object.get_filepath()
	elif path.endswith('/') == False:
		path = path + '/'

	### Find Files In Dir
	for file in os.listdir(path):
		if os.path.isfile(path + str(file)) == True and str(file).startswith('.') == False:
			choices.append(file)
	choices.append('[1] -- Specify New File Directory')
	choices.append('[0] Back')

	os.system('clear')
	click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')
	click.secho('Please Specify The File(s) You Wish To Use.', bold=True)
	click.echo('Currently Selected Path: ' + path + '\n')

	### If Attack Requires A Dictonary
	if pwd_object.get_attack() == 0 or pwd_object.get_attack() == 2 or pwd_object.get_attack() == 6 or pwd_object.get_attack() == 7:
		title = 'Please Select a Dictonary File'

		for dict_item in pwd_object.get_dict_list():
			click.echo(dict_item + ' Selected')

		index_selection = tms.generate_menu(title, choices)

		if index_selection == len(choices) - 1:
			PWD_attack_type(pwd_object)
		elif index_selection == len(choices) - 2:
			index_selection = tms.generate_dir_menu()
			if index_selection == '0':
				PWD_sel_dict(pwd_object)
			else:
				PWD_sel_dict(pwd_object, index_selection)
		else:
			pwd_object.add_dict_file(path + choices[index_selection])

	### If Attack Requires Multiple Dictonaries
	if pwd_object.get_attack() == 1:
		title = 'Please Select Multiple Dictonary Files (Max 2)'
		index_selection = tms.gernerate_multi_select_menu(title, choices, True)

		if index_selection[len(index_selection) - 1] == 'Back':
			PWD_attack_type(pwd_object)
		elif index_selection[len(index_selection) - 1] == '-- Specify New File Directory':
			index_selection = tms.generate_dir_menu()
			if index_selection == '0':
				PWD_sel_dict(pwd_object)
			else:
				PWD_sel_dict(pwd_object, index_selection)
		elif len(index_selection) > 2 or len(index_selection) < 2:
			index_selection = tms.generate_menu('Please Select 2 Dictonary Files! <ENTER>', '')
			PWD_sel_dict(pwd_object)
		else:
			for sel_dict in index_selection:
				pwd_object.add_dict_file(path + sel_dict)

	### If Attack Requires Rule File (Code 222 = loopback Prevention Code Due To Same Operation Attack code)
	if pwd_object.get_attack() == 2 or pwd_object.get_attack() == 222:
		title = 'Please Select a Rule File'
		choices.insert(len(choices) - 2, '[2] Nevermind, I Just Want A Dictonary')
		
		index_selection = tms.generate_menu(title, choices)

		if index_selection == len(choices) - 1:
			PWD_attack_type(pwd_object)
		elif index_selection == len(choices) - 2:
			index_selection = tms.generate_dir_menu()
			if index_selection == '0':
				PWD_sel_dict(pwd_object)
			else:
				pwd_object.set_attack(222)
				PWD_sel_dict(pwd_object, index_selection)
		elif index_selection == len(choices) - 3:
			pwd_object.set_sel_rule('')
		else:
			pwd_object.set_attack(0)
			pwd_object.set_sel_rule(path + choices[index_selection])

"""
Pwd_config_wizard goes through the list of settings realated to PWD and lets the user specify other options
will print and set options based on type of option and user selection
updates pwd_object with user selections
"""
def PWD_config_wizard(pwd_object):
	settings_list = scs.get_settings_list()
	new_settings_list = []

	###Collect Relevent Settings
	for setting in settings_list:
		if setting.get_section() == '----- Password Cracking Settings Settings -----':
			new_settings_list.append(setting)

	### Loop Through And Set Settings
	for setting in new_settings_list:
		title = '\n' + setting.get_description() + '\n'
		choices = []

		os.system('clear')
		click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')
		click.secho('Please Select The Setting Option You Wish To Set', bold=True)

		### Print If Setting = x
		if setting.get_code_call() == '$Default_Workload_Profile':
			click.echo(' * | Performance | Runtime | Power Consumption | Desktop Impact  ')	
			click.echo('===|=============|=========|===================|=================')	
			click.echo(' 1 | Low         |    2 ms | Low               | Minimal  ')	
			click.echo(' 2 | Default     |   12 ms | Econmice          | Noticeable  ')	
			click.echo(' 3 | High        |   96 ms | High              | Unresponsive  ')	
			click.echo(' 4 | Nightmare   |  480 ms | Insane            | Headless  ')

		if setting.get_code_call() == '$Max_Runtime':
			click.echo('0 = No Max Runtime')	
			click.echo('600 = 10 Minutes')	
			click.echo('3600 = 1 Hour')	
			click.echo('...')	
			click.echo('604800 = 1 Week')		
	
		for option in setting.get_items_list():
			choices.append(option)
		choices.append('[1] Use Default: {}'.format(str(setting.get_code().split(':')[1])))
		choices.append('[0] Back')

		index_selection = tms.generate_menu(title, choices)

		if index_selection == len(choices) - 1:
			PWD_config(pwd_object)
			break
		elif index_selection == len(choices) - 2:
			continue
		### Specify New Dir
		elif choices[index_selection].startswith('-- ') == True:
			index_selection = tms.generate_dir_menu()
			if index_selection == '0':
				PWD_config_wizard(pwd_object)
				break
			else:
				if index_selection.endswith('/') == False:
					index_selection = index_selection + '/'
				pwd_object.set_output_path(index_selection)
		### Set New Setting
		else:
			if setting.get_code_call() == '$Default_Workload_Profile':
				pwd_object.set_workload(choices[index_selection])
			if setting.get_code_call() == '$Optimised_Kernal':
				pwd_object.set_optimised_kernal(choices[index_selection])
			if setting.get_code_call() == '$Max_Runtime':
				pwd_object.set_max_runtime(int(choices[index_selection]))
			if setting.get_code_call() == '$Enable_Hashcat_Potfile':
				pwd_object.set_potfile(choices[index_selection])
		
"""
pwd_gen_mask is a charset/mask generator for bruteforce/hybrid attaks
uses hashcat built-in charsets and allows for creation of 4 custom charsets to use
updates pwd_object mask and custom charset list with user created options
"""
def PWD_gen_mask(pwd_object):
	os.system('clear')
	click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')
	click.secho('A Brute Force Attack Uses A Mask (Set Of Characters) To Check Every Combintion Within The Given Range', bold=True)
	click.echo('You Must Generate This Mask In Order To Brute Force. (?l?l?l?l Range = aaaa - zzzz)')
	click.echo('Each Charset "?l" Conatins a Set of Characters "?l = alphabet lowercase"')
	click.echo('Example: To Crack "Password1!", A mask Of "?u?l?l?l?l?l?l?l?d?s" Could Be Used!')
	click.echo('Please Use The Selections To Generate A Mask A character At A Time')
	click.echo('You Can Also Generate Custom Charsets To Add To The Mask!')
	click.echo('\nDefault Charsets:')
	click.echo('?l = abcdefghijklmnopqrstuvwxyz')
	click.echo('?u = ABCDEFGHIJKLMNOPQRSTUVWXYZ')
	click.echo('?d = 0123456789')
	click.echo('?h = 0123456789abcdef')
	click.echo('?H = 0123456789ABCDEF')
	click.echo('?s = Special Chars (/$#!...)')
	click.echo('?a = ?l?u?d?h')
	click.echo('?b = 0x00 - 0xff')

	### Loop Until Finished
	x = True
	while x:
		### Generate Charset Choices
		choices = ['?l','?u','?d','?h','?H','?s','?a','?b']
		charset_list = pwd_object.get_custom_charset_list()
		
		title = '\nCustom Charsets:\n'

		for count, charset in enumerate(charset_list):
			title = title + '?' + str(count + 1) + ' = ' + charset + '\n'
			choices.append('?{}'.format(str(count + 1)))

		title = title + '\nCurrent Mask:  ' + pwd_object.get_pass_mask() + '\n'
		choices.append('[3] Delete')
		choices.append('[2] Specify Custom Charset')
		choices.append('[1] Done')
		choices.append('[0] Back')		

		### Update mask On charset Selection
		index_selection = tms.generate_menu(title, choices)

		if index_selection == len(choices) - 1:
			PWD_attack_type(pwd_object)
			break
		elif index_selection == len(choices) - 2:
			if pwd_object.get_pass_mask() == '':
				index_selection = tms.generate_menu('\nPlease Select A valid Mask', '')
			else:
				break
		### Update Charset With New Custom created Charset (if applicable)
		elif index_selection == len(choices) - 3:
			if len(charset_list) > 3:
				choices2 = []
				for count, charset in enumerate(charset_list):
					choices2.append('[{}] Custom_Charset_{}: {}'.format(str(count +1), str(count +1), charset))
				index_selection = tms.generate_menu('\nMax Number Of Custom Charsets, Please Choose One To Replace', choices2)
				index_num = index_selection
			else:
				index_num = 9

			choices.pop(len(choices) - 3)
			for charset in charset_list:
				choices.pop(len(choices) - 4)

			### Generate Second Charset Menu To allow For creation of custom charset
			custom_charset = ''
			y = True
			while y:
				title = '\nCurrent Custom Charset:  ' + custom_charset + '\n'
				index_selection = tms.generate_menu(title, choices)
				
				if index_selection == len(choices) - 1:
					PWD_gen_mask(pwd_object)
					break
				elif index_selection == len(choices) - 2:
					if index_num == 9:
						if custom_charset == '':
							break
						else:
							pwd_object.add_custom_charset(custom_charset)
							break
					if index_num != 9:
						if custom_charset == '':
							break
						else:
							charset_list[index_num] = custom_charset
							pwd_object.set_custom_charset_list(charset_list)
							break
				elif index_selection == len(choices) - 3:
					curr_charset = custom_charset
					if curr_charset == '':
						pass
					else:
						custom_charset = curr_charset[:-2]
				else:
					custom_charset = custom_charset + choices[index_selection]
		### Delete End Charset (backspace)
		elif index_selection == len(choices) - 4:
			curr_mask = pwd_object.get_pass_mask()
			if curr_mask == '':
				pass
			else:
				pwd_object.set_pass_mask(curr_mask[:-2])
		else:
			curr_mask = pwd_object.get_pass_mask()
			pwd_object.set_pass_mask(curr_mask + choices[index_selection])