"""
Error Handling
Codes used to select the error with optional tags for similer errors
"""
import click

def error(code, tag):
	#1000: Invalid Seletion General Error
	if code == 1000:
		click.echo('Error: Invalid Selection. Please select a Valid option.')
	#1001: Wrong Drive Selection
	if code == 1001:
		click.echo('Error: No Drive Detected, Please Select Valid Drives.')
	#1002: Same Drive Acquisition & Storage Attempt
	if code == 1002:
		click.echo('Error: Cannot Aquire The Boot Drive Of This Device')
		click.echo('Hint: Override Disable in Settings.txt under Config/Settings.txt [Boot_Drive_Overide:True]')
	#1003: Settings File Fatal Error: Unable To Read Statement
	if code == 1003:
		click.echo('Settings.txt File Fatal Error: Unable To Read Statement')
		if tag == 1:
			click.echo('Error On Line: Boot_Drive_Override')
		if tag == 2:
			click.echo('Error On Line: Default_Tool')
	#1004: Unable To varify selected Directory
	if code == 1004:
		click.echo('Unable to verify directory. please select a valid Directory')
	

