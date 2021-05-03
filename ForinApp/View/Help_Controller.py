#Python Help Controller
#Application Name: Forin
#Author: J.Male
#Desc: 
#	Prints Help Information To The User.
#	Shows Install, What, How, And Possible Problems

import click
import sys
import os

from View import MainMenu_Controller
from Scripts import TerminalMenuScript as tms

"""
help_main_menu acts as the navigation menu for the secondary help menus
"""
def help_main_menu():
	os.system('clear')
	click.secho('Here To Help!\n', bold=True, fg='blue')
	click.echo('FORIN is a simple CLI app that allows you to perform quick/easy digital anylsis')
	click.echo('Mutiple Tools And Techniques Are used, If You Are unsure About Any Of the Tools, Please Select One Below:\n')
	click.echo('More Information, Inluding Any Replacement Files, Can be Found At:')
	click.echo('https://github.com/Jiskey/Raspberry-PI4-Forensics')
	click.echo('\nFinally! Thank You For Downloading Forin!')

	choices = ['[1] Acquire Image (Dc3dd / Dcfldd)', 
			'[2] File System Inspection (Sleuth Kit)',
			'[3] Data Carving (Foremost / Scalpel / PhotoRec)',
			'[4] PDF File Analysis (Pdfid / Pdf-Parser)',
			'[5] Password Cracking (Hashcat)', 
			'[0] Back']
	title = '\nWhat Can I Help You With?'
	selection_index = tms.generate_menu(title, choices)

	if selection_index == 0:
		help_img()
	elif selection_index == 1:
		help_fsi()
	elif selection_index == 2:
		help_dc()
	elif selection_index == 3:
		help_pdf()
	elif selection_index == 4:
		help_pwd()

	MainMenu_Controller.main_menu()

"""
display relevent help information for image acqusistion
"""
def help_img():
	os.system('clear')
	click.secho('Help: Acquire Image (Dc3dd / Dcfldd)\n', bold=True, fg='blue')
	click.echo('Drive Acqusition Is The Act Of Retriving The Data On A Computer Drive')
	click.echo('Connecting The Drive To This Device Will Allow You To Acquire All Or Part of its Data')
	click.echo('Drives Can Be Large And Take Time To Complete')
	click.echo('Ensure That The Device Has Enough space To Store The Data (Can Be Bigger Then The Actuall Drive)')
	
	click.secho('\nInstall Commands:', bold=True)
	click.echo('Debian: sudo apt-get install dc3dd')
	click.echo('        sudo apt-get install dcfldd\n')

	click.secho('\nUsage:', bold=True)
	click.echo('1. Ensure Tool Is Installed')
	click.echo('2. Connect Drive To This Device')
	click.echo('3. Select Either Full Drive Or A Drive Part(ition)')
	click.echo('4. Select Configuration Options')
	click.echo('5. Aquire Drive')

	index_selection = tms.generate_menu('\nPress ENTER to Continue.', '')
	help_main_menu()

"""
display relevent help information for file system inspection
"""
def help_fsi():
	os.system('clear')
	click.secho('Help: File System Inspection (Sleuth Kit)\n', bold=True, fg='blue')

	click.echo('File System Inspection Is looking Into A Forensic image To inspect The Files Contanied')
	click.echo('This is Done by Using Tools That Are Part of The Sleuth Kit')
	click.echo('If The Tools Can Obtain Its File System type (Not Corrupted) Then The Program Will Show its Contents')
	click.echo('If So, Then You Can Veiw The Contents Of The Image Including Directories & Deleted Images')
	click.echo('These Files Can Be Extracted For Closer Inspection')

	click.secho('\nInstall Commands:', bold=True)
	click.echo('Debian: sudo apt-get install sleuthkit')

	click.secho('\nUsage:', bold=True)
	click.echo('1. Ensure Tool Is Installed')
	click.echo('2. Select The Image File You Wish to Insepct')
	click.echo('3. (If Not Corrupt) Navigate The File System, selecting Dir & Files')
	click.echo('4. Export File Data')
	
	index_selection = tms.generate_menu('\nPress ENTER to Continue.', '')
	help_main_menu()

"""
display relevent help information for data carving
"""
def help_dc():
	os.system('clear')
	click.secho('Help: Data Carving (Foremost / Scalpel / PhotoRec)\n', bold=True, fg='blue')

	click.echo('Data Carving Is The Act Of Retriving Data From a Drive Based On A inupt')
	click.echo('The Input Is Usually Header Information That Defines Its File Type')
	click.echo('This Differs From FSI as Data Carving Is Used To Retive Data From A Corrupted Device')
	click.echo('Selecting Specfic Headers, if The data is Not Severly Damaged, There is a Chance it Can be Recovered')

	click.echo('\nNote: Scalpel Does Not Work Without Trouble Shooting On Device: Raspberry Pi 4\n')
	click.echo('Info: github.com/sleuthkit/scalpel/issues/11')

	click.secho('\nInstall Commands:', bold=True)
	click.echo('Debian: sudo apt-get install scalpel')
	click.echo('        sudo apt-get install foremost')
	click.echo('        sudo apt-get install photorec')

	click.secho('\nUsage:', bold=True)
	click.echo('1. Ensure Tool Is Installed')
	click.echo('2. Select The Image File You Wish to Carve')
	click.echo('3. Select Tool (PhotoRec is its Own Program')
	click.echo('4. Select header Types (Individualy or By Group)')
	click.echo('5. Carve Data From Drive')

	index_selection = tms.generate_menu('\nPress ENTER to Continue.', '')
	help_main_menu()

"""
display relevent help information for pdf file analysis
"""
def help_pdf():
	os.system('clear')
	click.secho('Help: PDF File Analysis (Pdfid / Pdf-Parser)\n', bold=True, fg='blue')

	click.echo('PDF Analysis Allows You To inspect The Contents Of a PDF file')
	click.echo('PDF Files Hold Lots Of Information such as owner, date, etc.')
	click.echo('However, PDF Files Can Contain Dangerous Payloads (Virus/Script)')
	click.echo('Viewing its Contents Without Ppening or Disarming The File Is Required To Prevent Possible damage')

	click.secho('\nInstall Commands:', bold=True)
	click.echo('Debian: sudo apt-get install pdf-parser')
	click.echo('        sudo apt-get install pdfid')

	click.secho('\nUsage:', bold=True)
	click.echo('1. Ensure Tool Is Installed')
	click.echo('2. Select The PDF File You Wish to Inspect')
	click.echo('3. (Program Will Process PDF File)')
	click.echo('4. Select What Type of Object To Inspect')
	click.echo('5. Choose object To Inspect')

	index_selection = tms.generate_menu('\nPress ENTER to Continue.', '')
	help_main_menu()

"""
display relevent help information for password cracking
"""
def help_pwd():
	os.system('clear')
	click.secho('Help: Password Cracking (Hashcat)\n', bold=True, fg='blue')

	click.echo('Hashcat Allows For Complex Cracking Of Hashes')
	click.echo('A Hash is An Unique Id for any peice Of Information (Including Passwords)')
	click.echo('Cracking These Hashing is Both Perfomance and Time Consuming')
	click.echo('Using Different Types Of Attack To Attampt To Crack hashes Using Rules, Dictonaries and masks')

	click.echo('\nNote: hashcat Requies OpenCL support. Which The Raspberry Pi4 Does Not Support By Default\n')
	click.echo('Info: hashcat.net/forum/thread-8116.html')

	click.secho('\nInstall Commands:', bold=True)
	click.echo('Debian: sudo apt-get install hashcat')

	click.secho('\nUsage:', bold=True)
	click.echo('1. Ensure Tool Is Installed')
	click.echo('2. Select The Hash File To Crack (Can Contain Mutliple Lines Of Hashes)')
	click.echo('3. Select The Hash Type (Must Be Known)')
	click.echo('4. Select Attack Type')
	click.echo('5. Depending on Attack: Either Select A Dictonary, Rule File, or generate A Mask')
	click.echo('6. Selection Configuration Options')
	click.echo('7. Start Cracking')

	index_selection = tms.generate_menu('\nPress ENTER to Continue.', '')
	help_main_menu()
			