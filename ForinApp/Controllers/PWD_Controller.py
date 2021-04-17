#Python 
#Application Name: Forin
#Author: J.Male
#Desc: 
#	

import click
import sys
import os

from View import MainMenu_Controller
from Model.PwdObject import PwdObject
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms
from Scripts import UsageLoggingScript as uls

"""

"""
def PWD_main_menu(path = '0'):
	choices = []
	title = ''
	if path and path != '0':
		evi_path = path
		if evi_path.endswith('/') == False:
			evi_path = evi_path + '/'
	else:
		evi_path = scs.settings_check('$Default_Output_Location')
		if evi_path.endswith('/') == False:
			evi_path = evi_path + '/'

	os.system('clear')
	click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')
	click.echo('Hashcat is a powerful hash cracking tool with many options to assist in this demanding task')
	click.echo('Password Cracking Is A very Demanding Task! Expect System Slowdown')	
	click.echo('\nCurrent Image Evidance Location: {}\n'.format(evi_path))

	title = 'Please Select A File That Contains The Hash Lines To Crack:'
	for file in os.listdir(evi_path):
		if os.path.isfile(evi_path + str(file)) == True and str(file).startswith('.') == False:
			choices.append(file)
	choices.append('[1] -- Specify Hash File Evidance Directory')
	choices.append('[0] Back')
	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		MainMenu_Controller.main_menu()
	elif index_selection == len(choices) - 2:
		index_selection = tms.generate_string_menu('Hash File Evidance Directory:', 1)
		if index_selection == '0':
			PWD_main_menu()
		else:
			PWD_main_menu(index_selection)

	pwd_object = PwdObject(evi_path, choices[index_selection])

	PWD_hash_type(pwd_object)
	PWD_attack_type(pwd_object)
	PWD_config(pwd_object)

"""

"""
def PWD_hash_type(pwd_object):
	choices = ['0 - MD5', '100 - SHA1', '1400 - SHA2-256', '1700 - SHA2-512', '1000 - NTLM' ,'[1] Select From List', '[0] back']
	title = '\nPlease Select The hash Type Of The Has You wish To Crack'	

	os.system('clear')
	click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')
	click.echo('You Must Know The hash Type before Attmepting To Crack')
	click.echo('Its Hard To Tell Which Hashes Are What Sometimes. Some do Have Identifers!')
	click.echo('MD5 Hash Example; baade50c0278b90b546974280789201a;')

	index_selection = tms.generate_menu(title, choices)

	if index_selection == 6:
		PWD_main_menu(pwd_object.get_filepath())
	elif index_selection == 5:
		PWD_hash_type_wizard(pwd_object)
	else:
		pwd_object.set_pass_hash(int(choices[index_selection].split()[0]))
"""

"""
def PWD_attack_type(pwd_object):
	title = '\nWhat Type Of Attack Would You Like To Take?'
	choices = ['[1] Dictonary','[2] Rules Based','[3] Combinator','[4] Brute Force','[5] Hybrid','[0] Back']

	os.system('clear')
	click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')

	click.echo('1. Dictonary Attack = Standard Dictonary Based Attack')
	click.echo('2. Rules Based Attack = Standard Dictonary Based Attack With A Set Of Rules')
	click.echo('3. Combinator Attack = Standard Dictonary Based Attack With Multiple Dicts (Concatination)')
	click.echo('4. Brute Force + Mask Attack = Brute Force Attack With The Use Of A Generated Mask')
	click.echo('5. Hybrid = Dictonary + Mask Attack OR Mask + Dictonary Attack')

	index_selection = tms.generate_menu(title, choices)

	if index_selection == 5:
		PWD_main_menu(pwd_object.get_filepath())
	if index_selection == 4:
		choices = ['[1] Mask:Dict','[2] Dict:Mask']
		title = '\nPlease Select A Format'
		index_selection = tms.generate_menu(title, choices)
		if index_selection == 0:
			pwd_object.set_attack(7)
		elif index_selection == 1:
			pwd_object.set_attack(6)
		PWD_sel_dict(pwd_object)
		PWD_gen_mask(pwd_object)
	if index_selection == 3:
		pwd_object.set_attack(3)
		PWD_gen_mask(pwd_object)
	if index_selection == 2:
		pwd_object.set_attack(1)
		PWD_sel_dict(pwd_object)
	if index_selection == 1:
		pwd_object.set_attack(2)
		PWD_sel_dict(pwd_object)
	if index_selection == 0:
		pwd_object.set_attack(0)
		PWD_sel_dict(pwd_object)
"""

"""
def PWD_config():
	pass

"""

"""
def PWD_hash_type_wizard(pwd_object):
	choices = []	
	title = 'Please Select The hash Type Of The Has You wish To Crack From The List'
	tmp_txt = ''	

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

	index_selection = tms.generate_menu(title, choices)
	
	if index_selection == len(choices) - 1:
		PWD_hash_type(pwd_object)
	else:	
		pwd_object.set_pass_hash(int(choices[index_selection].split()[0]))


"""

"""
def PWD_sel_dict(pwd_object, path = '0'):
	pwd_object.set_dict_list([])
	choices = []
	title = ''

	if path == '0':
		path = pwd_object.get_filepath()
	elif path.endswith('/') == False:
		path = path + '/'

	for file in os.listdir(path):
		if os.path.isfile(path + str(file)) == True and str(file).startswith('.') == False:
			choices.append(file)
	choices.append('[1] -- Specify New File Directory')
	choices.append('[0] Back')

	os.system('clear')
	click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')
	click.echo('Currently Selected Path: ' + path + '\n')


	if pwd_object.get_attack() == 0 or pwd_object.get_attack() == 2 or pwd_object.get_attack() == 6 or pwd_object.get_attack() == 7:
		title = 'Please Select a Dictonary File'

		for dict_item in pwd_object.get_dict_list():
			click.echo(dict_item + ' Selected')

		index_selection = tms.generate_menu(title, choices)

		if index_selection == len(choices) - 1:
			PWD_attack_type(pwd_object)
		elif index_selection == len(choices) - 2:
			index_selection = tms.generate_string_menu('Hash File Evidance Directory:', 1)
			if index_selection == '0':
				PWD_sel_dict(pwd_object)
			else:
				PWD_sel_dict(pwd_object, index_selection)
		else:
			pwd_object.add_dict_file(path + choices[index_selection])


	if pwd_object.get_attack() == 1:
		title = 'Please Select Multiple Dictonary Files (Max 2)'
		index_selection = tms.gernerate_multi_select_menu(title, choices, True)

		if index_selection[len(index_selection) - 1] == 'Back':
			PWD_attack_type(pwd_object)
		elif index_selection[len(index_selection) - 1] == '-- Specify New File Directory':
			index_selection = tms.generate_string_menu('Hash File Evidance Directory:', 1)
			if index_selection == '0':
				PWD_sel_dict(pwd_object)
			else:
				PWD_sel_dict(pwd_object, index_selection)
		elif len(index_selection) > 2:
			index_selection = tms.generate_menu('Please Select Only 2 Dictonary Files', '')
			PWD_sel_dict(pwd_object)
		else:
			for sel_dict in index_selection:
				pwd_object.add_dict_file(path + sel_dict)


	if pwd_object.get_attack() == 2 or pwd_object.get_attack() == 222:
		title = 'Please Select a Rule File'
		choices.insert(len(choices) - 2, '[2] Nevermind, I Just Want A Dictonary')
		
		index_selection = tms.generate_menu(title, choices)

		if index_selection == len(choices) - 1:
			PWD_attack_type(pwd_object)
		elif index_selection == len(choices) - 2:
			index_selection = tms.generate_string_menu('Hash File Evidance Directory:', 1)
			if index_selection == '0':
				PWD_sel_dict(pwd_object)
			else:
				pwd_object.set_attack(222)
				PWD_sel_dict(pwd_object, index_selection)
		else:
			pwd_object.set_attack(0)
			pwd_object.set_sel_rule(path + choices[index_selection])

"""

"""
def PWD_gen_mask(pwd_object):
	os.system('clear')
	click.secho('Password/Hash Cracking (Hashcat)\n', bold=True, fg='blue')
	click.echo('To Brute Force "Effectively", A Mask Is Required')
	click.echo('Please Use The Selections To Generate A Mask A character At A Time')
	click.echo('You Can Also Generate Custom Charsets!')
	click.echo('\nDefault Charsets:')
	click.echo('?l = abcdefghijklmnopqrstuvwxyz')
	click.echo('?u = ABCDEFGHIJKLMNOPQRSTUVWXYZ')
	click.echo('?d = 0123456789')
	click.echo('?h = 0123456789abcdef')
	click.echo('?H = 0123456789ABCDEF')
	click.echo('?s = Special Chars (/$#!...)')
	click.echo('?a = ?l?u?d?h')
	click.echo('?b = 0x00 - 0xff')

	x = True
	while x:
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

		index_selection = tms.generate_menu(title, choices)

		if index_selection == len(choices) - 1:
			PWD_attack_type(pwd_object)
			break
		elif index_selection == len(choices) - 2:
			if pwd_object.get_pass_mask() == '':
				index_selection = tms.generate_menu('\nPlease Select A valid Mask', '')
			else:
				break
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
		elif index_selection == len(choices) - 4:
			curr_mask = pwd_object.get_pass_mask()
			if curr_mask == '':
				pass
			else:
				pwd_object.set_pass_mask(curr_mask[:-2])
		else:
			curr_mask = pwd_object.get_pass_mask()
			pwd_object.set_pass_mask(curr_mask + choices[index_selection])







