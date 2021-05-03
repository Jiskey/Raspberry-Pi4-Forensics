#PwdObject Class Test File

import pytest
import sys
import os

from Model.PwdObject import *

def test_pwdsetting_class():
	filepath = '/home/kali/'
	filename = 'hashes.txt'

	pwd_object = PwdObject(filepath, filename)

	assert pwd_object.get_filepath() + pwd_object.get_filename() == '/home/kali/hashes.txt'

	pwd_object.gen_hash_list()
	assert len(pwd_object.get_hash_list()) > 10
	assert pwd_object.get_hash_list()[0].find('MD4') != -1

	pwd_object.set_workload('Low')
	assert pwd_object.get_workload() == 1
	pwd_object.set_workload(3)
	assert pwd_object.get_workload() == 3

	pwd_object.set_optimised_kernal('True')
	command = pwd_object.gen_command()
	assert command.startswith('sudo hashcat -O -w 3 -m 0 -a 0') == True
	assert command.find('/home/kali/hashes.txt') != -1