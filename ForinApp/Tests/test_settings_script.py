#Settings_Script Test File

import pytest

from Scripts.SettingsCheckScript import *

def test_get_settings_txt():
	txt_lines = get_settings_txt()
	assert type(txt_lines) == list
	assert len(txt_lines) > 0

def test_get_settings_list():
	settings_list = get_settings_list()
	assert type(settings_list) == list
	assert len(settings_list) > 0
	for setting in settings_list:
		assert type(setting) == Setting    #class
		assert type(setting.get_section()) == str
		assert type(setting.get_description()) == str
		assert type(setting.get_items()) == str
		assert type(setting.get_code()) == str
		assert setting.get_section().startswith('-----') != -1
		assert setting.get_description().startswith('#') != -1
		assert setting.get_items().startswith('[') != -1
		assert setting.get_code().startswith('$') != -1
		assert setting.get_code().find(':') != -1

def test_settings_check():
	txt_lines = get_settings_txt()
	for line in txt_lines:
		if line.startswith('$'):
			code, var = line.split(':')
			result = settings_check(code)
			assert type(result) == str
			assert result == var.strip('\n')

def test_settings_index():
	txt_lines = get_settings_txt()
	for count, line in enumerate(txt_lines):
		if line.startswith('$'):
			code, var = line.split(':')
			assert settings_index(code) == count		
			assert type(settings_index(code)) == int

def test_settings_update():
	txt_lines = get_settings_txt()
	settings_update(txt_lines)
	txt_lines2 = get_settings_txt()
	assert txt_lines == txt_lines2 
