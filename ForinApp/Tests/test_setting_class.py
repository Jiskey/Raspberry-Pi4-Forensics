#Settings_class Test File

import pytest

from Model.Setting import *

def test_setting_class():
	section = '----- Test Section -----'
	desc = '#Test Description'
	items = '[test][vars]'
	code = '$test:code'
	setting = Setting(section, desc, items, code)
	
	assert setting.get_section() == section
	assert setting.get_description() == desc
	assert setting.get_items() == items
	assert setting.get_code() == code

	assert setting.get_code_call() == '$test'
	assert setting.get_code_var() == 'code'
	set_list = setting.get_items_list()
	assert len(set_list) > 0
	assert set_list[0] == 'test' and set_list[1] == 'vars'

	setting.set_section(section + '1')
	setting.set_description(desc + '1')
	setting.set_items(items + '1')
	setting.set_code(code + '1')
	assert setting.get_section() == section + '1'
	assert setting.get_description() == desc  + '1'
	assert setting.get_items() == items + '1'
	assert setting.get_code() == code + '1'
