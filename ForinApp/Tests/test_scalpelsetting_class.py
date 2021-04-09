#Scalpel Settings_class Test File

import pytest

from Model.ScalpelSetting import *
from Scripts import ScalpelSettingsScript as sss

def test_setting_class():
	class_list = sss.get_DC_settings_list('Tests/test_dependencies/test_scalpel.conf')

	for sett in class_list:
		assert type(sett.get_cat()) == str
		assert type(sett.get_options()) == list
		for option in sett.get_options():
			assert type(option[0]) == str
			assert option[0] == '@' or '#'
			assert type(int(option[3])) == int
