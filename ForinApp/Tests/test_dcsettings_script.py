#Scalpel Settings Script Test File

import pytest

from Model.Setting import *
from Scripts import DcSettingsScript as dcss

def test_get_DC_settings_txt():
	txt_lines = dcss.get_DC_settings_txt('Tests/test_dependencies/test_scalpel.conf')
	assert type(txt_lines) == list
	assert len(txt_lines) > 0

def test_set_DC_settings_txt():
	txt_lines = dcss.get_DC_settings_txt('Tests/test_dependencies/test_scalpel.conf')
	dcss.set_DC_settings_txt(txt_lines, 'Tests/test_dependencies/test_scalpel.conf')
	new_txt_lines = dcss.get_DC_settings_txt('Tests/test_dependencies/test_scalpel.conf')
	assert txt_lines == new_txt_lines 

def test_get_DC_settings_list():
	class_list = dcss.get_DC_settings_list('Tests/test_dependencies/test_scalpel.conf')

	for sett in class_list:
		assert type(sett.get_cat()) == str
		assert type(sett.get_exts()) == list
		for ext in sett.get_exts():
			assert type(ext[0]) == str
			assert ext[0] == '@' or '#'
			assert type(int(ext[3])) == int

def test_set_DC_settings_list():
	class_list = dcss.get_DC_settings_list('Tests/test_dependencies/test_scalpel.conf')
	new_class_list = dcss.set_DC_settings_list(class_list, ('Select All', 'ext 14000 /0xx/0xx/0xx/?-ext'), 'adv')

	for sett in new_class_list:
		assert type(sett.get_cat()) == str
		assert type(sett.get_exts()) == list
		for ext in sett.get_exts():
			assert type(ext[0]) == str
			assert ext[0] == '@'
			assert type(int(ext[3])) == int

	for count, sett in enumerate(class_list):
		assert sett.get_cat() == new_class_list[count].get_cat()
		tmp_sett = new_class_list[count]
		for ext in sett.get_exts():
			assert tmp_sett.get_exts() != ext

def test_create_DC_settings_txt():
	class_list = dcss.get_DC_settings_list('Tests/test_dependencies/test_scalpel.conf')
	txt_lines = dcss.get_DC_settings_txt('Tests/test_dependencies/test_scalpel.conf')
	new_txt = dcss.create_DC_settings_txt(txt_lines, class_list)

	for count, line in enumerate(txt_lines):
		assert line == new_txt[count]
	
