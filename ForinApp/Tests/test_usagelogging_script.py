#UsageLog_Script Test File

import pytest

from Scripts import UsageLoggingScript as uls
from Scripts import SettingsCheckScript as scs

def test_log_change():
	filepath = scs.settings_check('$Default_Hash_Logging_Location')
	filepath_new = filepath + 'Usage_Logs/README.txt'
	contents = ''

	txt = open(filepath_new, 'r') 
	cmp_contents = txt.read()
	txt.close()
	
	action = 'Settings_Change'
	uls.log_change(filepath_new, action, contents)
	txt = open(filepath_new, 'r') 
	new_contents = txt.read()
	txt.close()
	assert new_contents == cmp_contents

	action = 'Acq_Attempt'
	uls.log_change(filepath_new, action, contents)
	txt = open(filepath_new, 'r') 
	new_contents = txt.read()
	txt.close()
	assert new_contents == cmp_contents
