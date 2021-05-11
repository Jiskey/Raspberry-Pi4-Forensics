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
	click.secho('FORIN Is A Simple CLI Application That Allows You To Perform Quick/Easy Digital Anylsis', bold=True)
	click.echo('Mutiple Tools And Techniques Are Used, If You Are unsure About Any Of The Tools, Please Select One Below:\n')
	click.echo('All Configuration Options Can be Found Under Config/Settings.txt')
	click.echo('\nThe App Has Been Developed And Designed To Work With Kali Linux (Debian) However, If Another Linux Distro is Used')
	click.echo('And The Tools Are Installed, They Should Still Work And The App Should Function Correctly.')	
	click.echo('\nMore Information, Inluding Any Replacement Files, And Known Errors/Bugs Can be Found At:')
	click.echo('https://github.com/Jiskey/Raspberry-PI4-Forensics')
	click.echo('\nForin Has Beed Realised Under The MIT License.')
	click.echo('\nFinally! Thank You For Downloading Forin!')

	choices = ['[1] Acquire Image (Dc3dd / Dcfldd)', 
			'[2] File System Inspection (Sleuth Kit)',
			'[3] Data Carving (Foremost / Scalpel / PhotoRec)',
			'[4] PDF File Analysis (Pdfid / Pdf-Parser)',
			'[5] Password Cracking (Hashcat)', 
			'[0] Back']
	title = '\nWhat Can I Help You With?'
	index_selection = tms.generate_menu(title, choices)

	if index_selection == 0:
		help_acq()
	elif index_selection == 1:
		help_fsi()
	elif index_selection == 2:
		help_dc()
	elif index_selection == 3:
		help_pdf()
	elif index_selection == 4:
		help_pwd()

	MainMenu_Controller.main_menu()

"""
display relevent help information for image acqusistion
"""
def help_acq():
	os.system('clear')
	click.secho('Help: Acquire Image (Dc3dd / Dcfldd)\n', bold=True, fg='blue')
	click.secho('Drive Acqusition Is The Act Of Retriving The Data On A Computer Drive', bold=True)
	click.echo('Connecting The Drive To This Device Will Allow You To Acquire All Or Part Of Its Data')
	click.echo('Drives Can Be Large And Take Time To Complete')
	click.echo('Ensure That The Device Has Enough space To Store The Data (Can Be Bigger Then The Actuall Drive)')
	click.echo('Sometimes, Fdisk Can Get Boot Drives Incorrect! If You Dont See The Drive When Its Conneted, Try Disabling Boot_Override In The Settings')
	click.secho('\nInstall Commands:', bold=True)
	click.echo('Debian: sudo apt-get install dc3dd')
	click.echo('        sudo apt-get install dcfldd\n')
	click.echo('Program Default Evidance Output: Evidance/ACQ_Evidance')
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
	click.secho('File System Inspection Is looking Into A Forensic image To inspect The Files Contanied', bold=True)
	click.echo('This is Done by Using Tools That Are Part of The Sleuth Kit')
	click.echo('If The Tools Can Obtain Its File System type (Not Corrupted) Then The Program Will Show its Contents')
	click.echo('If So, Then You Can Veiw The Contents Of The Image Including Directories & Deleted Images')
	click.echo('These Files Can Be Extracted For Closer Inspection')
	click.secho('\nInstall Commands:', bold=True)
	click.echo('Debian: sudo apt-get install sleuthkit')
	click.echo('Program Default Evidance Output: Evidance/FSI_Evidance')
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
	click.secho('Data Carving Is The Act Of Retriving Data From a Drive Based On A inupt', bold=True)
	click.echo('The Input Is Usually Header Information That Defines Its File Type (.Png /x50/x4e/x47)')
	click.echo('This Differs From FSI as Data Carving Is Used To Retive Data From A Corrupted Device')
	click.echo('Selecting Specfic Headers, if The data is Not Severly Damaged, There is a Chance it Can be Recovered')
	click.echo('\nNote: Scalpel Does Not Work Without Trouble Shooting On Device: Raspberry Pi 4')
	click.echo('Info: github.com/sleuthkit/scalpel/issues/11')
	click.secho('\nInstall Commands:', bold=True)
	click.echo('Debian: sudo apt-get install scalpel')
	click.echo('        sudo apt-get install foremost')
	click.echo('        sudo apt-get install photorec')
	click.echo('Program Default Evidance Output: Evidance/DC_Evidance')
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
	click.secho('PDF Analysis Allows You To inspect The Contents Of a PDF file', bold=True)
	click.echo('PDF Files Hold Lots Of Information such as owner, date, etc. Contined In "Objects" Conatined in "Streams"')
	click.echo('However, PDF Files Can Contain Dangerous Payloads (Virus/Script)')
	click.echo('Viewing its Contents Without Opening or Disarming The File Is Required To Prevent Possible damage')
	click.secho('\nInstall Commands:', bold=True)
	click.echo('Debian: sudo apt-get install pdf-parser')
	click.echo('        sudo apt-get install pdfid')
	click.echo('Program Default Evidance Output: Evidance/PDF_Evidance')
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
	click.secho('Hashcat Allows For Complex Cracking Of Hashes And Passwords!', bold=True)
	click.echo('A Hash is An Unique Id for any peice Of Information (Including Passwords)')
	click.echo('Cracking These Hashing is Both Perfomance and Time Consuming')
	click.echo('Using Different Types Of Attack To Attampt To Crack hashes Using Rules, Dictonaries and masks')
	click.echo('\nNote: hashcat Requies OpenCL support. Which The Raspberry Pi4 Does Not Support By Default')
	click.echo('Info: hashcat.net/forum/thread-8116.html')
	click.secho('\nInstall Commands:', bold=True)
	click.echo('Debian: sudo apt-get install hashcat')
	click.echo('Program Default Evidance Output: Evidance/PWD_Evidance')
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
			