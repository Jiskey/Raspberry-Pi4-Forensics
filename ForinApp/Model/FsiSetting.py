#Python FsiSetting Model (File System Inspection)
#Application Name: Forin
#Author: J.Male
#Desc: 
#	FsiSetting Model Contains, Stores & Edits Information From/For FSI_Controller.
#	Contains Data From Multiple TSK Tool Outputs

import os
import sys

"""
Fsi Setting Class
Holds and handles data required for use with the sleuth kit (TSK)
"""
class FsiSetting:
	img_name = ''
	img_ext = ''
	file_path = ''	
	img_format = ''		
	img_FS_format = ''
	output_path = ''
	byte_offset = 0
	fsstat_txt = []
	fls_txt = []
	mmls_txt = []
	fls_list = []
	inode_nav_list = []
	sel_inode = 0;
	sel_indoe_ext = ''
	output_path = ''		

	def __init__(self, img_name, img_ext, file_path, img_format, img_FS_format, output_path):
		self.img_name = img_name
		self.img_ext = img_ext
		self.file_path = file_path
		self.img_format = img_format
		self.img_FS_format = img_FS_format
		self.output_path = output_path

	def get_img_name(self):					# Img.dd Name
		return self.img_name

	def get_img_ext(self):					# Img.dd Ext.
		return self.img_ext
		
	def get_file_path(self):				# Img.dd File Path
		return self.file_path

	def get_img_format(self):				# Img.dd Format (exam: dos)
		return self.img_format

	def get_img_FS_format(self):				# Img.dd File System Format
		return self.img_FS_format

	def get_output_path(self):				# Evidance Output Path
		return self.output_path

	def get_byte_offset(self):				# Img.dd Byte Offset
		return self.byte_offset

	def get_fsstat_txt(self):				# Str Lines From fsstat Command
		return self.fsstat_txt

	def get_mmls_txt(self):					# Str Lines From mmls Command
		return self.mmls_txt

	def get_fls_txt(self):					# Str Lines From fls Command
		return self.fls_txt

	def get_fls_list(self):					# List of fls items
		return self.fls_list

	def get_fls(self, fls_num):				# Single fls item ([*][inode][name]...)
		return self.fls_list[fls_num]

	def get_inode_nav_list(self):				# List of previously selected inodes
		return self.inode_nav_list

	def add_inode_nav(self, inode):	
		self.inode_nav_list.append(inode)

	def del_inode_nav(self, inode):				
		self.inode_nav_list.pop(inode)

	def get_sel_inode(self):				# The Currently Selected inode
		return self.sel_inode

	def set_sel_inode(self, sel_inode):			
		self.sel_inode = sel_inode

	### Sets fsstat_txt With File Lines
	def set_fsstat(self, fsstat_txt):
		self.fsstat_txt = fsstat_txt

	### Sets Both mmls_txt With File Lines And Updates mmls_list
	def set_mmls(self, mmls_txt):
		self.mmls_txt = mmls_txt

	### Sets Both fls_txt With File Lines And Updates fls_list
	def set_fls(self, fls_txt):
		self.fls_txt = fls_txt

		self.fls_list = []
		for line in fls_txt:
			tmp = {
				"type": "",
				"deleted": "",
				"inode": "",
				"name": ""
			}
			file_name = ''
			line = line.split()
			if line[1] != '*':
				tmp['type'] = line[0].strip()
				tmp['inode'] = int(line[1].strip(':'))
				file_name = ''
				for count, txt in enumerate(line):
					if count > 1:
						file_name += ' ' + txt
				tmp['name'] = file_name
			else:
				tmp['type'] = line[0].strip()
				tmp['deleted'] = line[1].strip()
				tmp['inode'] = int(line[2].strip(':'))
				for count, txt in enumerate(line):
					if count > 2:
						file_name += ' ' + txt
				tmp['name'] = file_name.strip()
			self.fls_list.append(tmp)

	### Generates The ffstat information To Append
	def gen_ffstat(self, path):
		os.system('fsstat -i ' + self.img_format + ' -f ' + self.img_FS_format + ' ' + self.file_path + ' > ' + self.output_path + self.img_name + '_details.txt')
		for line in open(self.output_path + self.img_name + '_details.txt'):
			if line.startswith('FAT CONTENTS'):
				break
			self.fsstat_txt.append(line.strip())
		else:
			self.fls_txt.append('\n')
	
	### Generates The mmls information To Append
	def gen_mmls(self, path):
		os.system('mmls -i ' + self.img_format + ' ' + self.file_path + ' >> ' + self.output_path + self.img_name + '_details.txt')
		os.system('mmls -i ' + self.img_format + ' ' + self.file_path + ' > Config/tmp.txt' )
		for line in open('Config/tmp.txt'):
			self.mmls_txt.append(line)
		else:
			self.fls_txt.append('\n')
		os.system('rm Config/tmp.txt')

	### Generates The fls information To Append
	def gen_fls(self, path):
		os.system('fls -i ' + self.img_format + ' -f ' + self.img_FS_format + ' ' + self.file_path + ' >> ' + self.output_path + self.img_name + '_details.txt')
		os.system('fls -i ' + self.img_format + ' ' + self.file_path + ' > Config/tmp.txt' )
		for line in open('Config/tmp.txt'):
			self.fls_txt.append(line)
		else:
			self.fls_txt.append('\n')
		os.system('rm Config/tmp.txt')

	### Update fls List With New List Based On Selection
	def update_fls(self, inode):
		fls_txt = []
		if inode != 0:
			os.system('fls -i ' + self.img_format + ' -f ' + self.img_FS_format + ' ' + self.file_path + ' ' + str(inode) + ' > Config/tmp.txt')
		else:
			os.system('fls -i ' + self.img_format + ' ' + self.file_path + ' > Config/tmp.txt' )
		for line in open('Config/tmp.txt'):
			fls_txt.append(line)
		os.system('rm Config/tmp.txt')
		self.set_fls(fls_txt)

	### Export istat Output To File & Save 
	def export_istat(self):
		os.system('istat -i ' + self.img_format + ' -f ' + self.img_FS_format + ' ' + self.file_path + ' ' + str(self.sel_inode) + ' > ' + self.output_path + str(self.sel_inode) + '_istat.txt')

	### Export icat Hexdump Output To File & Save 
	def export_icat_hex(self):
		os.system('icat -i ' + self.img_format + ' -f ' + self.img_FS_format + ' ' + self.file_path + ' ' + str(self.sel_inode) + ' | hexdump > ' + self.output_path + str(self.sel_inode) + '_icat.txt')

	### Export icat Image Output To File & Save 
	def export_icat_img(self, file_ext):
		os.system('icat -i ' + self.img_format + ' -f ' + self.img_FS_format + ' ' + self.file_path + ' ' + str(self.sel_inode) + ' > ' + self.output_path + str(self.sel_inode) + '_icat.' + file_ext.strip())
