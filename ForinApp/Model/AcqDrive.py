#Python AcqDrive Class
#Application Name: Forin
#Author: J.Male
#Desc: 
#	Drive Class Is the Class That holds collected from / created in F-disk script.
#	Also Creates a Command To Execute For Obtain A Drive Using Dc3dd / Dcfldd

import sys
import os

from Scripts import SettingsCheckScript as scs

"""
Acq Drive Class
Holds Drive and handles data required for use with the Dc3dd / Dcfldd
Also Creates a Command To Execute
"""
class AcqDrive:
	path = ''						
	size = 0
	size_bytes = 0
	sectors = 0
	model = ''
	sector_size = ''
	disklabel = ''
	identifier = ''
	boot = False
	partitions = [];

	def __init__(self, path, size, size_bytes, sectors, model, sector_size, disklabel, identifier, boot, partitions):
		self.path = path						
		self.size = size
		self.size_bytes = size_bytes
		self.sectors = sectors
		self.model = model
		self.sector_size = sector_size
		self.disklabel = disklabel 
		self.identifier = identifier 
		self.boot = boot
		self.partitions = partitions

#Gets (Will Never Set)
	def get_path(self):				
		return self.path

	def get_size(self):				
		return self.size

	def get_size_bytes(self):			
		return self.size_bytes
	
	def get_sectors(self):				
		return self.sectors

	def get_model(self):				
		return self.model

	def get_sector_size(self):			
		return self.sector_size

	def get_disklabel(self):				
		return self.disklabel

	def get_identifier(self):			
		return self.identifier

	def get_boot(self):				
		return self.boot

	def get_partitions(self):			
		return self.partitions

	def get_partition(self, part):
		return self.partitions[part]
	
	### Get Partition Path
	def get_partition_path(self, part):
		part_path, part_start, part_end, part_type = self.partitions[part].split(':')
		return part_path
	
	### Get Partition Sectors Start
	def get_partition_start(self, part):
		part_path, part_start, part_end, part_type = self.partitions[part].split(':')
		return int(part_start)

	### Get Partition Sectors End
	def get_partition_end(self, part):				
		part_path, part_start, part_end, part_type = self.partitions[part].split(':')
		return int(part_end)

	### Get Partition Sectors
	def get_partition_sectors(self, part):	
		part_path, part_start, part_end, part_type = self.partitions[part].split(':')
		part_sectors = (int(part_end) - int(part_start)) + 1
		return int(part_sectors)

	### Get Partition Sectors Size (GB)
	def get_partition_size(self, part):				
		part_path, part_start, part_end, part_type = self.partitions[part].split(':')
		part_sectors = (int(part_end) - int(part_start)) + 1
		part_sectors = part_sectors * 512
		part_sectors = part_sectors / 1024
		part_sectors = part_sectors / 1024
		part_sectors = part_sectors / 1024
		return float(part_sectors)

	### Get Partition Sectors Size (bytes)
	def get_partition_size_bytes(self, part):
		part_path, part_start, part_end, part_type = self.partitions[part].split(':')
		part_sectors = (int(part_end) - int(part_start)) + 1
		part_sectors = part_sectors * 512
		return int(part_sectors)

	### Get Partition Sector Type
	def get_partition_type(self, part):
		part_path, part_start, part_end, part_type = self.partitions[part].split(':')
		return part_type

	### Get Logical Sector Size
	def get_sector_size_log(self):		
		log, pyhs = self.sector_size.split(':')
		return int(log)

	### Get Physical Sector Size
	def get_sector_size_pyhs(self):
		log, pyhs = self.sector_size.split(':')
		return int(pyhs)

	### Command_gen Generates a Command String To Execute In The Console (Dc3dd / Dfcldd)
	def gen_command(self, settings_list, p_code): 
		tool = ''		
		name = ''
		output_loc = ''
		otf_hashing = ''
		hash_mode = ''
		enable_logs = ''
		hash_log_loc = ''
		multi_hash = ''
		hash_mode_2 = ''
		byte_split = ''
		file_split = ''
		split_size = ''
		split_format = ''
		hash_conv = ''
		error = ''

		### Collect Dependincies
		for count, setting in enumerate(settings_list):
			if setting.get_code_call() == '$Default_Tool':
				tool = setting.get_code_var()
			elif setting.get_code_call() == '$Default_Image_Name':
				name = setting.get_code_var()
			elif setting.get_code_call() == '$Default_Output_Location':
				output_loc = setting.get_code_var()
			elif setting.get_code_call() == '$Enable_OTF_Hashing':
				otf_hashing = setting.get_code_var()
			elif setting.get_code_call() == '$Enable_Logging':
				enable_logs = setting.get_code_var()
			elif setting.get_code_call() == '$Hashing_Mode':
				hash_mode = setting.get_code_var()
			elif setting.get_code_call() == '$Default_Hash_Logging_Location':
				hash_log_loc = setting.get_code_var()
			elif setting.get_code_call() == '$Multiple_Hashing':
				multi_hash = setting.get_code_var()
			elif setting.get_code_call() == '$Hashing_Mode_2':
				hash_mode_2 = setting.get_code_var()
			elif setting.get_code_call() == '$Byte_Split':
				byte_split = setting.get_code_var()
			elif setting.get_code_call() == '$File_Splitting':
				file_split = setting.get_code_var()
			elif setting.get_code_call() == '$Split_Size':
				split_size = setting.get_code_var()
			elif setting.get_code_call() == '$Split_Format':
				split_format = setting.get_code_var()
			elif setting.get_code_call() == '$Hashing_Conversion':
				hash_conv = setting.get_code_var()
			elif setting.get_code_call() == '$Error_handling':
				error = setting.get_code_var()

		try:
			check = 0
			tmp = name.strip()
			for count, file in enumerate(os.listdir(output_loc)):	
				if file.startswith(tmp) and file.endswith('.dd'):
					check = check + 1
			else:
				name = tmp + str(check)
		except:
			pass
		
		if hash_log_loc.endswith('/') == False:
			hash_log_loc += '/'
		if output_loc.endswith('/') == False:	
			output_loc += '/'

		### Start Of Command
		start = 'sudo {} '.format(tool)						
		if p_code == 255:
			part = self.get_path()					
		else:
			part = self.get_partition_path(p_code)
		drive = 'if={} '.format(part)
		output = 'of={}'.format(output_loc)
		if output.endswith('/'):
			output += name + '.dd '
		else: 
			output += '/' + name + '.dd '
		if otf_hashing == 'True':
			hashing = 'hash={} '.format(hash_mode)
		else:
			hashing = ''
		if enable_logs == 'True' and otf_hashing == 'True':			
			log = 'log={}{}.log '.format(hash_log_loc, name)	
		else:
			log = ''

		### Generatate Dc3dd Command
		output = '"' + output.strip() + '"'
		command = start + drive + output + hashing + log

		if tool == 'dcfldd':
			if multi_hash == 'True' and hash_mode_2 != hash_mode:		
				hashing = hash_mode + ',' + hash_mode_2 + ' '
				if enable_logs == 'True':
					log = '{}log={}{}_{}.txt '.format(hash_log_loc, hash_mode, name, hash_mode)
					log += '{}log={}{}_{}.txt '.format(hash_log_loc, hash_mode_2, name, hash_mode_2)
				else:
					log = ''
			elif multi_hash == 'True' and hash_mode_2 == hash_mode:		
				if enable_logs == 'True':
					log = '{}log={}_{}.txt '.format(hash_mode, name, hash_mode)
				else:
					log = ''
			elif multi_hash == 'False':					
				if enable_logs == 'True':
					log = '{}log={}_{}.txt '.format(hash_mode, name, hash_mode)
				else:
					log = ''

			if file_split == 'True': 
				splitting = 'split={} '.format(split_size)
				splitting_format = 'splitformat={} '.format(split_format)
				hash_window = 'hashwindow={} '.format(split_size)
			else:
				splitting = ''
				splitting_format = ''
				hash_window = ''

			if error == 'True':						
				error_handling = 'conv=noerror,sync '
			else:
				error_handling = ''
			converstion = 'hashconv={} '.format(hash_conv)
			block_size = 'bs={} '.format(byte_split)	

			### Generate Dcfldd Command
			output = '"' + output.strip() + '"'
			command = start + drive + hashing + log + hash_window + converstion + block_size + error_handling + splitting + splitting_format + output
		
		return command