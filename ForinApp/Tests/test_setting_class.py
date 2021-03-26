#Settings_class Test File

import pytest

from Classes.Setting import *

def test_setting_class_gets_sets():
	section = '----- Test Section -----'
	desc = '#Test Description'
	items = '[test][vars]'
	code = '$test:code'
	setting = Setting(section, desc, items, code)
	
	assert setting.get_section() == section
	assert setting.get_description() == desc
	assert setting.get_items() == items
	assert setting.get_code() == code

	setting.set_section(section + '1')
	setting.set_description(desc + '1')
	setting.set_items(items + '1')
	setting.set_code(code + '1')

	assert setting.get_section() == section + '1'
	assert setting.get_description() == desc  + '1'
	assert setting.get_items() == items + '1'
	assert setting.get_code() == code + '1'
