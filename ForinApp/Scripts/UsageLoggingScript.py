#Python Usage Logging Script
#Whenever a user changes somthing in the app or executes a function, a log will be made

import click
import sys
import os
import time

from Scripts import SettingsCheckScript as scs
"""
simple logging function.
requires the filepath, the name of the change (action), list of lines to write to file
Latest change is appended to the start of the list
"""
def log_change(filepath, action, contents):
	localtime = time.asctime(time.localtime(time.time()))
	output = "--- Action Taken: {} AT: {} BY: Guest\n".format(action, localtime)
	exsisting_logs = []

	try:
		txt = open(filepath, 'r')		#retrive already stored lines
		for line in txt:
			exsisting_logs.append(line)
		txt.close()
	except:
		pass

	if action == 'Settings_Change':
		txt = open(filepath, 'w')		#write setting new log
		if contents != '':		
			txt.write(output)
			for item in contents:
				item = item.get_code()
				code, var = item.split(':')
				oldvar = scs.settings_check(code)
				txt.write('Settings Changed: {}   From: {}   To: {}\n'.format(code, oldvar, var))
			txt.write('\n')
		txt == open(filepath, 'a')
		for item in exsisting_logs:		#append old logs
			txt.write(item)
		txt.close()

	if action == 'Acq_Attempt' and contents != '':
		txt = open(filepath, 'w')		#write Acq new log
		if contents != '':
			txt.write(output)
			txt.write('Command Used: {}'.format(contents))
			txt.write('\n')
		txt == open(filepath, 'a')
		for item in exsisting_logs:		
			txt.write(item)
		txt.close()
			
