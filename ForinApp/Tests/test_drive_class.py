#Drive_class Test File

import pytest

from Classes.Drive import *
from Scripts import FdiskScript as fds 

"""
Class That tests the Drive Class
WILL NOT WORK ON OTHER SYSTEMS... CURRENT ASSERSTIONS ARE BASED ON PC BOOT DRIVE
"""
def test_drive_class_gets():

	drives = fds.fdisk()
	
	assert len(drives) >= 1
	assert len(drives) > 1
	assert drives[0].get_path() == '/dev/sda'
	assert drives[0].get_size() == 465.76
	assert drives[0].get_size_bytes() == 500107862016
	assert drives[0].get_sectors() == 976773168
	assert drives[0].get_model() == ''
	assert drives[0].get_sector_size() == '512:4096'
	assert drives[0].get_disklabel() == 'dos'
	assert drives[0].get_identifier().find('a8ce') != 1 
	assert drives[0].get_boot() == True
	assert drives[0].get_partition(0) == '/dev/sda1:2048:262143:W95 FAT32 (LBA)'
	assert drives[0].get_sector_size_log() == 512
	assert drives[0].get_sector_size_pyhs() == 4096

	assert len(drives[0].get_partitions()) > 0
	assert drives[0].get_partition_path(0) == '/dev/sda1'
	assert drives[0].get_partition_start(0) == 2048
	assert drives[0].get_partition_end(0) == 262143
	assert drives[0].get_partition_sectors(0) == 260096
	assert drives[0].get_partition_size(0) == 0.1240234375
	assert drives[0].get_partition_size_bytes(0) == 133169152
	assert drives[0].get_partition_type(0) == 'W95 FAT32 (LBA)'
