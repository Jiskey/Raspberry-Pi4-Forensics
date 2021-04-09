#CommandCreationScript.py Test File

import pytest
import os
import sys

from Scripts import CommandCreationScript as ccs
from Scripts import FdiskScript as fds
from Scripts import SettingsCheckScript as scs

def test_acq_command_gen():
	settings_list = scs.get_settings_list()
	new_settings_list = []
	new_settings_list.clear()

	drives_list = fds.fdisk(False, False)

	check = 0
	for setting in settings_list:
		if setting.get_section() == '----- Acqusisition Settings -----':
			new_settings_list.append(setting)

	cmd = ccs.acq_command_gen(new_settings_list, drives_list[0], 255)
	assert type(cmd) == str
	assert cmd.find('dc3dd') != -1 or cmd.find('dcfldd') != -1
	assert cmd.find('sudo') != -1
	assert cmd.find('if=') != -1
	assert cmd.find('of=') != -1
	assert cmd.find('.img') != -1

def test_DC_commmand_gen():
	conf_path = '/this/is/a/path'
	tool = 'foremost'
	dir_name = 'this/is/outdir'
	carve_path = 'this/file/to/carve'

	cmd = ccs.DC_commmand_gen(conf_path, tool, dir_name, carve_path)
	assert type(cmd) == str
	assert cmd == 'sudo foremost -T -v -c /this/is/a/path this/file/to/carve -o this/is/outdir/'
	
	tool = 'scalpel'
	cmd = ccs.DC_commmand_gen(conf_path, tool, dir_name, carve_path)
	assert type(cmd) == str
	assert cmd == 'sudo scalpel -v -c /this/is/a/path this/file/to/carve -o this/is/outdir/'

def test_PDF_pdfid_command_gen():
	path = 'Config/'
	filename = 'file.txt'

	cmd = ccs.PDF_pdfid_command_gen(path, 'True', filename)
	assert type(cmd) == str
	assert cmd == 'sudo pdfid -d Config/file.txt -o Config/file_pdfid.txt'
	os.system('sudo rm ' + path + 'file_pdfid.txt')
	
def test_PDF_pdfparser_objs_command_gen():
	path = '/this/is/a/path/'
	filename = 'test.txt'

	cmd = ccs.PDF_pdfparser_objs_command_gen(path, filename)
	assert type(cmd) == str
	assert cmd == 'sudo pdf-parser -c -O /this/is/a/path/test.txt > /this/is/a/path/test_parser_objs.txt'

def test_PDF_pdfparser_locs_command_gen():
	path = '/this/is/a/path/'
	filename = 'test.txt'

	cmd = ccs.PDF_pdfparser_locs_command_gen(path, filename)
	assert type(cmd) == str
	assert cmd == 'sudo pdf-parser -a -O /this/is/a/path/test.txt > /this/is/a/path/test_parser_locs.txt'

def PDF_pdfparser_hash_command_gen(path, filename):
	path = '/this/is/a/path/'
	filename = 'test.txt'

	cmd = ccs.PDF_pdfparser_locs_command_gen(path, filename)
	assert type(cmd) == str
	assert cmd == 'sudo pdf-parser -H /this/is/a/path/test.txt > /this/is/a/path/test_parser_md5.txt'





