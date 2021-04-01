#CommandCreationScript.py Test File

import pytest

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
	assert cmd.find('sudo') != -1
	assert cmd.find('if=') != -1
	assert cmd.find('of=') != -1
	assert cmd.find('.img') != -1
	
