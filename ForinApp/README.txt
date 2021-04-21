######################################################################################################
___ ___  ___             _      ___ _  _            _   _           _           
| __/ _ \| _ \___ _ _  __(_)__  |_ _| \| |_ _____ __| |_(_)__ _ __ _| |_ ___ _ _ 
| _| (_) |   / -_) ` \(_-< / _|  | || .` \ V / -_|_-<  _| / _` / _` |  _/ _ \ `_|
|_| \___/|_|_\___|_||_/__/_\__| |___|_|\_|\_/\___/__/\__|_\__, \__,_|\__\___/_|  
                                                          |___/                  
FORIN - KALI LINUX DIGITAL FORENSIC INVESTIGATOR
By: J. Male
Version: 0.7.4 22/04/2021
Kali Version: 2021.1
Desc: "FORIN" is a simple CLI app that allows you to perform quick/easy digital anylsis and
	investigation using the tools included with Kali Linux

More Information: https://github.com/Jiskey/Raspberry-PI4-Forensics

######################################################################################################

ALL SUB FOLDERS SHOULD HAVE A FILE CALLED '__init__.py' THAT SHOULD BE EMTPY (Github does not like emtpy files are folders)

As Of Kali v2021.1, the Following Issues Are Needed To Be Resolved Before Use:

Scalpel:
	Scalpel Does Not Work On The Raspberry Pi Without Troubleshooting.

Missing Tools:
	Kali v2021.1 For The Raspberry Pi Removed These Tools When Updating From v2020.4:
		Dc3dd
		Dcfldd
		Foremost
	These Tools Can Be Installed With: "sudo apt-get install [Tool]"