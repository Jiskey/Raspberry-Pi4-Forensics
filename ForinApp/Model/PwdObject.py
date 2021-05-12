#Python PwdObject Class
#Application Name: Forin
#Author: J.Male
#Desc: 
#	PWD_Object Class Hold and handles operation involved wht password cracking (PWD)
#	Contains information About Attack types and files to use.

import sys
import os

from Scripts import SettingsCheckScript as scs

"""
pwd_object class handles and edits information needede to performa password cracking.
contains hashes, files, attack codes, ...
Includes hashcat command generation and has_list generation
"""
class PwdObject:
	filepath = ''
	filename = ''
	output_path = ''
	pass_hash = 0
	pass_mask = ''
	dict_list = []
	sel_rule = ''
	custom_charset_list = []
	attack = 0
	workload = 1
	optimised_kernal = 'False';
	hash_list = []
	max_runtime = 0
	potfile = 'True'

	def __init__(self, filepath, filename):
		self.filepath = filepath
		self.filename = filename

	def get_filepath(self):				
		return self.filepath

	def get_filename(self):				
		return self.filename

	def get_output_path(self):				
		return self.output_path

	def set_output_path(self, output_path):				
		self.output_path = output_path

	def get_pass_hash(self):
		return self.pass_hash

	def set_pass_hash(self, pass_hash):
		self.pass_hash = pass_hash

	def get_pass_mask(self):				
		return self.pass_mask

	def set_pass_mask(self, pass_mask):				
		self.pass_mask = pass_mask

	def get_dict_list(self):				
		return self.dict_list

	def set_dict_list(self, dict_list):				
		self.dict_list = dict_list

	def add_dict_file(self, dict_file):
		self.dict_list.append(dict_file)

	def get_dict_file(self, dict_file):
		return self.dict_list[dict_file]

	def get_sel_rule(self):				
		return self.sel_rule

	def set_sel_rule(self, sel_rule):				
		self.sel_rule = sel_rule

	def get_custom_charset_list(self):				
		return self.custom_charset_list

	def set_custom_charset_list(self, custom_charset_list):				
		self.custom_charset_list = custom_charset_list

	def add_custom_charset(self, charset):
		self.custom_charset_list.append(charset)

	def get_attack(self):				
		return self.attack

	def set_attack(self, attack):				
		self.attack = attack

	def get_workload(self):				
		return self.workload

	def set_workload(self, workload):
		if type(workload) == int:				
			self.workload = workload
		elif workload == 'Low':
			self.workload = 1
		elif workload == 'Default':
			self.workload = 2
		elif workload == 'High':
			self.workload = 3
		elif workload == 'Nightmare':
			self.workload = 4

	def get_optimised_kernal(self):				
		return self.optimised_kernal

	def set_optimised_kernal(self, optimised_kernal):				
		self.optimised_kernal = optimised_kernal

	def get_hash_list(self):				
		return self.hash_list

	def set_hash_list(self, hash_list):				
		self.hash_list = hash_list

	def get_max_runtime(self):
		return self.max_runtime

	def set_max_runtime(self, max_runtime):
		self.max_runtime = max_runtime

	def get_potfile(self):
		return self.potfile

	def set_potfile(self, potfile):
		self.potfile = potfile

	### Command that generates the hashes compbatible with Hashcat
	def gen_hash_list(self):
		check = False
		tmp_string = ''

		os.system('hashcat --help > Config/tmp.txt')
		tmp = open('Config/tmp.txt')
		os.system('sudo rm Config/tmp.txt')

		for line in tmp:
			if line.strip() == '- [ Hash modes ] -':
				check = True
			elif line.strip() == '- [ Brain Client Features ] -':
				check = False
				break
			split_line = line.split()
			try:
				if int(split_line[0]) and split_line[1] == '|' and check == True:
					self.hash_list.append(line.strip())
			except:
				continue

	### Generate Hashcat command
	def gen_command(self):
		command = 'sudo hashcat '
		if self.potfile == 'False':
			command = command + '--potfile-disable '
		if self.max_runtime != 0:
			command = command + '--runtime={} '.format(self.max_runtime)
		if self.optimised_kernal == 'True':
			command = command + '-O '
		command = command + '-w {} '.format(self.workload)
		command = command + '-m {} '.format(self.pass_hash)
		command = command + '-a {} '.format(self.attack)
		if self.sel_rule != '':
			command = command + '-r "{}" '.format(self.sel_rule)
		command = command + '-o "{}{}"'.format(self.output_path, self.filename.split('.')[0] + '_evidance.txt')
		command = command + ' "{}"'.format(self.filepath + self.filename)

		if self.attack == 0 or self.attack == 1:
			for wordlist in self.dict_list:
				command = command + ' "' + wordlist + '" '
		elif self.attack == 3 or self.attack == 6 or self.attack == 7:
			if self.attack == 6:
				for wordlist in self.dict_list:
					command = command + ' "' + wordlist + '" '

			for count, charset in enumerate(self.custom_charset_list):
				command = command + '-' + str(count + 1) + ' ' + charset + ' '
			command = command + self.pass_mask + ' '

			if self.attack == 7:
				for wordlist in self.dict_list:
					command = command + ' "' + wordlist + '" '

		return command




