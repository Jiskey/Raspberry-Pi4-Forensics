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
	pass_hash = ''
	pass_mask = ''
	custom_charset_1 = ''
	custom_charset_2 = ''
	custom_charset_3 = ''
	custom_charset_4 = ''
	workload = 1
	opencl_type = 1
	optimised_kernal = False;

	def __init__(self, filepath, filename):
		self.filepath = filepath
		self.filename = filename

	def get_filepath(self):				
		return self.filepath

	def get_filename(self):				
		return self.filename