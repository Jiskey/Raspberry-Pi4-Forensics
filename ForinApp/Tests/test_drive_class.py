#Drive_class Test File

import pytest

from Classes.Drive import *

def test_drive_class_gets_sets():
	num = 0
	path = '/dev/sda'
	size = 128
	sizebytes = 134000000
	drive = Drive(num, path, size, sizebytes)

	assert drive.get_number() == num
	assert drive.get_path() == path
	assert drive.get_size_gb() == size
	assert drive.get_size_bytes() == sizebytes

	drive.set_number(num + 1)
	drive.set_path(path + '1')
	drive.set_size_gb(size + 1)
	drive.set_size_bytes(sizebytes + 1)

	assert drive.get_number() == num + 1
	assert drive.get_path() == path + '1'
	assert drive.get_size_gb() == size + 1
	assert drive.get_size_bytes() == sizebytes + 1

def test_drive_class_partitions():
	num = 0
	path = '/dev/sda'
	size = 128
	sizebytes = 134000000
	drive = Drive(num, path, size, sizebytes)

	partitions = ['/dev/sda1', '/dev/sda2', '/dev/sda3']
	drive.add_drive_partition(partitions[0])
	assert len(drive.get_partitions()) == 1
	drive.add_drive_partition(partitions[1])
	drive.add_drive_partition(partitions[2])
	assert len(drive.get_partitions()) == 3

	drive.set_partition_selection(partitions[1])
	assert drive.get_partition_selection() == partitions[1]

	drive.del_drive_partition(partitions[1])
	assert len(drive.get_partitions()) == 2
	assert drive.get_partitions()[1] == partitions[2]
