#GUI_Controller
#Desc: Handles Execution Of GUI elements within the application.

import click
import sys
import os

#Generate Application Header
def main_menu(count):
	os.system('clear')

	click.echo('\n######################################################################################################')
	click.secho('    ___ ___  ___             _      ___ _  _            _   _           _           ', bold=True)
	click.secho('   | __/ _ \| _ \___ _ _  __(_)__  |_ _| \| |_ _____ __| |_(_)__ _ __ _| |_ ___ _ _ ', bold=True)
	click.secho('   | _| (_) |   / -_) ` \(_-< / _|  | || .` \ V / -_|_-<  _| / _` / _` |  _/ _ \ `_|', bold=True)
	click.secho('   |_| \___/|_|_\___|_||_/__/_\__| |___|_|\_|\_/\___/__/\__|_\__, \__,_|\__\___/_|  ', bold=True)
	click.secho('                                                             |___/                  ', bold=True) 
	click.secho('\n-  FORIN - KALI LINUX DIGITAL FORENSIC INVESTIGATOR', bold=True, fg='blue')
	click.echo('-  By: J. Male')
	click.echo('-  Version 0.0.1: 15/12/2020')
	click.echo('-  Kali Version: 2020.4')
	click.echo('-  Desc: "FORIN" is a simple CLI app that allows you to perform quick/easy digital anylsis and')
	click.echo('         investigation using the tools included with Kali Linux')
	click.echo('\n-  More Information: https://github.com/Jiskey/Raspberry-PI4-Forensics')
	click.echo('\n######################################################################################################')
	click.echo('\nIMPORTANT NOTE: BE SURE TO RUN AS SU!')

#Generate Main Menu Options
	click.echo('\nWelcome! What Would You Like To Do?')
	click.echo('\n1 - Aquire A New Image')
	click.echo('2 - Analyse Exsisting Image')
	click.echo('3 - Settings')
	click.echo('0 - Exit')

#Detect User Selection with attmept counter (With 'easter-egg')
	x = False
	while x == False:
		selection = input('\n--- ')

		if selection == '1':
			code = 'ACQ'
			break
		elif selection == '2':
			sys.exit(0)
			x = True
		elif selection == '3':
			sys.exit(0)
			x = True
		elif selection == '0' :
			sys.exit(0)
			x = True
		else:
			count = count + 1
			if count < 5:
				click.echo('Please select a valid option')
			elif count < 10:
				click.echo('Are you okay? Is there a problem?')
			elif count < 15:
				click.echo('Perhaps English is not your first language?')
			elif count < 20:
				click.echo('Okay, now your just messing with me!')
			elif count < 25:
				click.echo('Thats it! Ive had enough!')
			elif count >= 26:
				click.echo('...')

	return code









