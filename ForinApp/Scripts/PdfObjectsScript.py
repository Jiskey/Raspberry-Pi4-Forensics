#Python PDF Objects Script
#Application Name: Forin
#Author: J.Male
#Desc: 
#	Used to create files and infomration about PDF Objects generated from Pdfid & Pdf-Parser

import click
import sys
import os
import time

from Model.PdfObject import PdfObject
from Scripts import SettingsCheckScript as scs

"""
pdf objects list creates a list of objs based on files created by the tool commands.
reads these output files to extract data and contain that in a PdfObject class.
for live previewing, a txt file will be created for each obj, contianed in a created Dir.
requires a path where the pdf is located (evidance), the name of the selected file, and check if hashing is enabled
returns a list of PdfObject's and a path for each file location 
"""
def get_pdf_objects_list(evi_path, sel_file, hash_check):
	path = evi_path + sel_file[:-4]				
	objs_path = path + '_parser_objs.txt'
	locs_path = path + '_parser_locs.txt'
	hash_path = path + '_parser_md5.txt'
	pdfid_path = path + '_pdfid.txt'
	paths = []
	obj_id = 0
	header_lines = []
	data_lines = []
	content_lines = []
	pdf_objects_list = []
	w_check = ''
	head_check = False
	data_check = False

	### Open Tool Generated Files
	txt = open(objs_path)					
	txt_objs_lines = txt.readlines()
	txt.close()
	txt = open(locs_path)					
	txt_loc_lines = txt.readlines()
	txt.close()
	try:
		txt = open(hash_path)				
		txt_hash_lines = txt.readlines()
		txt.close()
	except:
		pass

	dir_path = path + '_parser_objs'
	if dir_path.endswith('/') == False:
		dir_path += '/'
	os.system('sudo mkdir ' + dir_path)
	os.system('sudo rm ' + dir_path + '*')

	### Create PDF Object Files
	for count, line in enumerate(txt_objs_lines):
		try:
			if txt_objs_lines[count + 1].startswith('obj ') == True:
				pdf_objects_list.append(PdfObject(obj_id, header_lines, data_lines, content_lines))
				obj_id = 0
				header_lines = []
				data_lines = []
				content_lines = []
				w_check = ''
				head_check = False
				data_check = False
		except:
			pass

		if line.startswith('obj '):
			obj_id = line.split()
			obj_id = obj_id[1]
			obj_id = int(obj_id)
			w_check = 'head'
		elif line.startswith('  <<\n') == True and head_check == True:
			w_check = 'data'

		if w_check == 'head':
			header_lines.append(line)
			if line.startswith('\n'):
				w_check == ''
				head_check = True
				continue
		if w_check == 'data':
			data_lines.append(line)
			if line.startswith('  >>'):
				w_check = ''
				data_check = True
				continue

		if data_check == True and head_check == True and line.startswith('\n') == False:
			content_lines.append(line)

		if line.startswith('trailer'):
			break

	### Delete 'False' Objects
	try:
		pdf_objects_list.pop(0)
		pdf_objects_list.append(PdfObject(obj_id, header_lines, data_lines, content_lines))
	except:
		pass

	### Append Found Tags & MD5 hashses from tool generated Files
	stream = ''
	for line in txt_loc_lines:
		try:
			if line.find(':') != -1 and line.startswith(' ') == True:
				tmp = line.split(':')
				stream = tmp[0]
				codes = tmp[1] 
				codes = codes.split(',')
				for code in codes:
					code = int(code.strip())
					for obj in pdf_objects_list:
						if obj.get_id() == code:
							if stream.find(' ') != -1:
								new_stream = stream.split()
								obj.set_tag(new_stream[0].strip())
							else:
								obj.set_tag(stream.strip())
		except:
			continue

	if hash_check == 'True':
		hash_list = []
		for count, line in enumerate(txt_hash_lines):
			try:
				if line.startswith('obj '):
					obj_line = line.split()
					obj_code = obj_line[0]
					hash_line = txt_hash_lines[count + 1]
					hash_line = hash_line.split()
					obj_hash = hash_line[len(hash_line) - 1]
					hash_list.append(obj_code + ':' + obj_hash)
			except:
				pass

		for saved_hash in hash_list:	
			saved_hash = saved_hash.split(':')
			for obj in pdf_objects_list:
				if obj.get_id() == int(saved_hash[0]):
					obj.set_md5(saved_hash[1])

	### Create Files For Storage & Preview
	for obj in pdf_objects_list:
		txt = open(dir_path + '/obj_{}.txt'.format(obj.get_id()), 'w')
		for line in obj.get_head():
			txt.write(line)
		for line in obj.get_data():
			txt.write(line)
		txt.write('\n')
		for line in obj.get_contents():
			txt.write(line)
		txt.write('\nMD5 : ' + obj.get_md5())
		txt.close()

	paths.append(hash_path)
	paths.append(locs_path)
	paths.append(objs_path)
	paths.append(dir_path)
	paths.append(pdfid_path)
	return pdf_objects_list, paths

