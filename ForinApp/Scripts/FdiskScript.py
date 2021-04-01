#Python Fdisk Script
#Used whenever the app requries data about drives connected to the device

import click
import sys
import os

from Scripts import SettingsCheckScript as scs

from Classes.Drive import Drive

"""
Returns a list of drives connected to the device
uses fdisk -l command + string formatings of output file to retrive data
prints the full fdisk.txt file text (VERBOSE)
"""
def fdisk(verbose = False, print_text = True):
	os.system('sudo fdisk -l > Config/fdisk_search.txt')
	txt = open('Config/fdisk_search.txt','r')
	txt_lines = txt.readlines()
	txt.close()

	drive_list = []						#list to store drive classes

	path = ''						#Drive Class Details To Save
	size = 0
	size_bytes = 0
	sectors = 0
	model = 'Unknown'
	sector_size = ''
	disklabel = ''
	identifier = ''
	boot = False
	partitions = []

	v_details = ''
	details = ''
	check = 0
	drive_found = False
	for line in txt_lines:
		v_details += line
		if drive_found == True and check < 2:
			details += line
			if line.startswith('\n'):
				check = check + 1				#Check of 2 == New Device	
			if line.startswith('Disk model:'):				#store model
				a, model = line.split(':')
				model = model.strip()
			if line.startswith('Sector size'):				#store sector size
				a, b = line.split(':')
				log, phys = b.split('/')
				log, b = log.split()
				phys, b = phys.split()
				sector_size = log.strip() + ':' + phys.strip()
			if line.startswith('Disklabel type:'):			#store label
				a, disklabel = line.split(':')
				disklabel = disklabel.strip()
			if line.startswith('Disk identifier'):			#store identifier
				a, identifier = line.split(':')
				identifier = identifier.strip()
			if line.startswith('Device') and check == 1 and line.find('Boot') != -1:	#check for boot
				boot = True
			if line.startswith(path1.strip(':')) == True:					#store partition details
				part_details = line.split()
				part_path = part_details[0].strip()
				part_start = part_details[1].strip()
				part_end = part_details[2].strip()
				part_type = ''
				for count, part in enumerate(part_details):				#Format Partition to gather details
					if boot == True:
						check2 = 6
					else:
						check2 = 5
					if count >= check2:
						part_type += part + ' '
				part_type.strip()
				partitions.append((part_path + ':' + part_start + ':' + part_end + ':' + part_type).strip())
		else:
			if check == 2:
				drive_list.append(Drive(path, size, size_bytes, sectors, model, sector_size, disklabel, identifier, boot, partitions))
				check = 0
				path = ''			
				size = 0
				size_bytes = 0
				sectors = 0
				model = 'Unknown'
				sector_size = ''
				disklabel = ''
				identifier = ''
				boot = False
				partitions = []
				drive_found = False	
			if line.startswith('Disk /') and line.find('ram') == -1:	#Find Disc & Ignore Ram
				details += line
				drive_found = True
				a, path1, size1, b, size_bytes1, c, sectors1, d = line.split()
				path1 = path1.strip()
				path = path1.strip(':')
				size = float(size1.strip())
				size_bytes = int(size_bytes1.strip())
				sectors = int(sectors1.strip())
			else:
				continue
	else:
		if drive_list[len(drive_list) - 1].get_identifier() != identifier:	#Append Final Drive When EOF reached
			drive_list.append(Drive(path, size, size_bytes, sectors, model, sector_size, disklabel, identifier, boot, partitions))

	if print_text == True:
		if verbose == True:
			click.echo(v_details)
		else:
			click.echo(details)

	return drive_list
	
