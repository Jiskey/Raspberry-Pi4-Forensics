#UsageLog_Script Test File

import pytest
import os
import sys

from Scripts import UsageLoggingScript as uls
from Scripts import SettingsCheckScript as scs

def test_log_change():
	filepath = scs.settings_check('$Default_UsageLog_Location')
	if filepath.endswith('/') == False:
		filepath += '/'
	filepath_new = filepath + 'test.txt'
	contents = ''

	txt = open(filepath_new, 'w') 
	txt.write('TestLine1\n')
	txt.write('TestLine2\n')
	txt.write('TestLine3\n')
	txt.close()
	
	action = 'Settings_Change'
	uls.log_change(filepath_new, action, contents)
	txt = open(filepath_new, 'r') 
	new_contents = txt.readlines()
	txt.close()
	assert new_contents[len(new_contents) - 1].strip() == 'TestLine3'
	assert new_contents[0].find('Settings_Change') != -1

	action = 'Acq_Attempt'
	uls.log_change(filepath_new, action, contents)
	txt = open(filepath_new, 'r') 
	new_contents = txt.readlines()
	txt.close()
	assert new_contents[len(new_contents) - 1].strip() == 'TestLine3'
	assert new_contents[0].find('Acq_Attempt') != -1

	action = 'Data_Carve_Attempt'
	uls.log_change(filepath_new, action, contents)
	txt = open(filepath_new, 'r') 
	new_contents = txt.readlines()
	txt.close()
	assert new_contents[len(new_contents) - 1].strip() == 'TestLine3'
	assert new_contents[0].find('Data_Carve_Attempt') != -1

	action = 'PDF_Parse_Attmept'
	uls.log_change(filepath_new, action, contents)
	txt = open(filepath_new, 'r') 
	new_contents = txt.readlines()
	txt.close()
	assert new_contents[len(new_contents) - 1].strip() == 'TestLine3'
	assert new_contents[0].find('PDF_Parse_Attmept') != -1

	os.system('rm ' + filepath_new)
	assert os.path.isfile(filepath_new) == False
