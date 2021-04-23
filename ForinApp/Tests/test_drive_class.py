#Drive_class Test File

import pytest

from Model.AcqDrive import *
from Scripts import FdiskScript as fds 
from Scripts import SettingsCheckScript as scs

def test_drive_class():

	drives = fds.fdisk(False, False)
	
	assert len(drives) >= 1
	assert len(drives) > 1
	assert type(drives[0].get_path()) == str
	assert type(drives[0].get_size()) == float
	assert type(drives[0].get_size_bytes()) == int
	assert type(drives[0].get_sectors()) == int
	assert type(drives[0].get_model()) == str
	assert type(drives[0].get_sector_size()) == str
	assert type(drives[0].get_disklabel()) == str
	assert type(drives[0].get_identifier()) == str 
	assert type(drives[0].get_boot()) == bool
	assert type(drives[0].get_partition(0)) == str
	assert type(drives[0].get_sector_size_log()) == int
	assert type(drives[0].get_sector_size_pyhs()) == int

	assert len(drives[0].get_partitions()) > 0
	assert type(drives[0].get_partition_path(0)) == str
	assert type(drives[0].get_partition_start(0)) == int
	assert type(drives[0].get_partition_end(0)) == int
	assert type(drives[0].get_partition_sectors(0)) == int
	assert type(drives[0].get_partition_size(0)) == float
	assert type(drives[0].get_partition_size_bytes(0)) == int
	assert type(drives[0].get_partition_type(0)) == str

def test_acq_gen_command():
	settings_list = scs.get_settings_list()
	new_settings_list = []
	new_settings_list.clear()

	drives_list = fds.fdisk(False, False)

	check = 0
	for setting in settings_list:
		if setting.get_section() == '----- Acqusisition Settings -----':
			new_settings_list.append(setting)

	cmd = drives_list[0].gen_command(new_settings_list, 255)
	assert type(cmd) == str
	assert cmd.find('dc3dd') != -1 or cmd.find('dcfldd') != -1
	assert cmd.find('sudo') != -1
	assert cmd.find('if=') != -1
	assert cmd.find('of=') != -1
	assert cmd.find('.dd') != -1
	assert cmd.find(drives_list[0].get_path())
