#FsiSetting Class Test File

import pytest
import sys
import os

from Model.FsiSetting import *
from Scripts import SettingsCheckScript as scs

def test_fsisetting_class():
	file_path = 'Tests/test_dependencies/tmp.dd'
	fsi_path = 'Tests/test_dependencies/'
	output_path = fsi_path
	file_details = file_path.split('/')
	name, ext = file_details[len(file_details) - 1].split('.')

	os.system('img_stat -t ' + file_path + ' > Tests/test_dependencies/tmp.txt')
	for line in open('Tests/test_dependencies/tmp.txt'):
		img_format = line.strip()
	os.system('fsstat -t -i ' + img_format + ' ' + file_path + ' > Tests/test_dependencies/tmp.txt')
	for line in open('Tests/test_dependencies/tmp.txt'):
		img_FS_format = line.strip()
	os.system('sudo rm Tests/test_dependencies/tmp.txt')

	img_conf = FsiSetting(name, ext, file_path, img_format, img_FS_format, output_path)

	assert os.path.isfile('Tests/test_dependencies/tmp.txt') == False
	assert type(img_conf.get_img_name()) == str
	assert type(img_conf.get_img_ext()) == str
	assert type(img_conf.get_file_path()) == str
	assert type(img_conf.get_img_format()) == str
	assert type(img_conf.get_img_FS_format()) == str

	img_conf.gen_fsstat(fsi_path)
	img_conf.gen_fls(fsi_path)
	img_conf.update_fls(0)
	os.system('sudo rm Tests/test_dependencies/tmp.txt')
	os.system('sudo rm Tests/test_dependencies/tmp_details.txt')

	assert os.path.isfile('Tests/test_dependencies/tmp.txt') == False
	assert os.path.isfile('Tests/test_dependencies/tmp_details.txt') == False
	assert type(img_conf.get_fsstat_txt()) == list
	assert type(img_conf.get_fsstat_txt()[0]) == str
	assert type(img_conf.get_fls_txt()) == list
	assert type(img_conf.get_fls_txt()[0]) == str

	assert type(img_conf.get_fls_list()) == list
	assert type(img_conf.get_fls(0)) == dict
	assert type(img_conf.get_fls(0)['type']) == str
	assert type(img_conf.get_fls(1)['deleted']) == str
	assert type(img_conf.get_fls(1)['inode']) == str
	assert type(img_conf.get_fls(0)['name']) == str
	tmp_inode = img_conf.get_fls(0)['inode']

	for fls in img_conf.get_fls_list():
		if fls['type'].startswith('d/'):
			inode_code = fls['inode']
			break

	img_conf.update_fls(inode_code)
	assert type(img_conf.get_fls_list()) == list
	assert type(img_conf.get_fls(0)) == dict
	assert type(img_conf.get_fls(0)['type']) == str
	assert type(img_conf.get_fls(0)['deleted']) == str
	assert type(img_conf.get_fls(0)['inode']) == str and img_conf.get_fls(0)['inode'] != tmp_inode
	assert type(img_conf.get_fls(0)['name']) == str
	