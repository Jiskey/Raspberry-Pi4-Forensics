#Drive_class Test File

import pytest

from Model.Drive import *
from Scripts import FdiskScript as fds 

def test_drive_class_gets():

	drives = fds.fdisk()
	
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
