#Scalpel Settings_class Test File

import pytest

from Model.DcObject import *
from Scripts import DcSettingsScript as dcss

def test_setting_class():
	class_list = dcss.get_DC_settings_list('Tests/test_dependencies/test_scalpel.conf')

	for sett in class_list:
		assert type(sett.get_cat()) == str
		assert type(sett.get_exts()) == list
		for ext in sett.get_exts():
			assert type(ext[0]) == str
			assert ext[0] == '@' or '#'
			assert type(int(ext[3])) == int
