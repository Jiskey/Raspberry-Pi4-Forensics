#Python PwdObject Class
#Application Name: Forin
#Author: J.Male
#Desc: 
#	
#	

import sys
import os

from Scripts import SettingsCheckScript as scs

"""

"""
class PwdObject:
	filepath = ''
	filename = ''
	output_path = ''
	pass_charset = ''
	pass_hash = 0
	pass_mask = ''
	dict_list = []
	sel_rule = ''
	custom_charset_list = []
	attack = 0
	workload = 1
	opencl_type = 1
	optimised_kernal = False;
	hash_list = []

	def __init__(self, filepath, filename):
		self.filepath = filepath
		self.filename = filename

	def get_filepath(self):				
		return self.filepath

	def get_filename(self):				
		return self.filename

	def get_output_path(self):				
		return self.output_path

	def get_pass_charset(self):
		return self.pass_charset

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

	def get_opencl_type(self):				
		return self.opencl_type

	def get_optimised_kernal(self):				
		return self.optimised_kernal

	def get_hash_list(self):				
		return self.hash_list

	def set_hash_list(self, hash_list):				
		self.hash_list = hash_list

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
