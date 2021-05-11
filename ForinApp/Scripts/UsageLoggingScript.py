#Python Usage Logging Script
#Application Name: Forin
#Author: J.Male
#Desc: 
#	Whenever a user changes somthing in the app or executes a function, a log will be made
#	This Is usualy after the primary action of the application


import click
import sys
import os
import time

from Scripts import SettingsCheckScript as scs

"""
Usage Logging Function.
This Function Takes a filepath a turns it into a log (Appending old Information) Recording The Time.
A Usage Log Is Called After a User Uses A Feature In The Program (Usually After Warning Prompt)
Requires The filepath, the name of the change (action) and contents to write to file
"""
def log_change(filepath, action, contents):
	localtime = time.asctime(time.localtime(time.time()))
	output = "--- Action Taken: {} AT: {} BY: {}\n".format(action, localtime, scs.settings_check('$Operation_Name'))
	exsisting_logs = []

	try:
		txt = open(filepath, 'r')		
		for line in txt:
			exsisting_logs.append(line)
		txt.close()
	except:
		pass

	### Log When Settings Are Changes
	if action == 'Settings_Change':
		txt = open(filepath, 'w')		
		if contents != '':		
			txt.write(output)
			for item in contents:
				item = item.get_code()
				code, var = item.split(':')
				oldvar = scs.settings_check(code)
				txt.write('Settings Changed: {}   From: {}   To: {}\n'.format(code, oldvar, var))
			txt.write('\n')
		else:
			txt.write(output)

	### Log When Executing ACQ Tools
	if action == 'Acq_Attempt':
		txt = open(filepath, 'w')
		if contents != '':		
			txt.write(output)
			txt.write('Command Used: {}'.format(contents))
			txt.write('\n')
		else:
			txt.write(output)

	### Log When Executing DC Tools
	if action == 'Data_Carve_Attempt':
		txt = open(filepath, 'w')
		if contents != '':		
			txt.write(output)
			txt.write('Command Used: {}'.format(contents[0]))
			txt.write(contents[1])
			txt.write('\n')
		else:
			txt.write(output)

	### Log After Generation of PDF objects
	if action == 'PDF_Parse_Attmept':
		txt = open(filepath, 'w')
		if contents != '':		
			txt.write(output)
			for x in contents:
				txt.write('Command: ' + x)
			txt.write('\n\n')
		else:
			txt.write(output)

	### Log After Generation of FSI Tool Files
	if action == 'File_System_Inspection':	
		txt = open(filepath, 'w')
		if contents != '':
			txt.write(output)
			txt.write('File Inspected: ' + contents)
			txt.write('\n')

	### Log After Attempt At Password Cracking (PWD)
	if action == 'Password_Crack_Attempt':	
		txt = open(filepath, 'w')
		if contents != '':
			txt.write(output)
			txt.write('Command Used: ' + contents)
			txt.write('\n')

	txt = open(filepath, 'a')
	for item in exsisting_logs:		
		txt.write(item)
	txt.close()
