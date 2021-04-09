#Python DC_Controller (Data Carving)
#Desc: Handles all of the operations within the application realting to Data Carving

import click
import sys
import os

from View import MainMenu_Controller
from Model.PdfObject import PdfObject
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms
from Scripts import CommandCreationScript as ccs
from Scripts import UsageLoggingScript as uls
from Scripts import PdfObjectsScript as pos

"""
DC_main_menu is first page requests the user to select a tool.
NOTE: AS OF KALI V2020.4 For The Pi4. SCALPLE DOES NOT FUNCTION WITHOUT TROUBLESHOOTING
requires a path that can be empty.
"""
def PDF_main_menu(*path):
	if path and path != '0':
		evi_path = path
	else:
		evi_path = scs.settings_check('$PDF_Evidance_Location')			#gen path if empty

	os.system('clear')
	click.secho('PDF File Analysis\n', fg='blue', bold=True)

	click.echo('Pdfid and pdf-parser will scan a pdf file and Forin will display its output')
	click.echo('This Will Create A Disarmed PDF Copy, a .txt file containing the PDF objects & a txt of object locations')
	click.echo('these files can be found in the same dir as the PDF evidance.\n')

	click.echo('Note: In Order For Forin To Display Information, Txt Files Will be created FOR EACH OBJ in the pdf')
	click.echo('      This Can Have An Effect On Process Time With Larger PDF Files.\n')

	hashes = scs.settings_check('$PDF_Hashes')
	click.echo('Enable Object MD5 Hashes: {}'.format(hashes))

	disarm = scs.settings_check('$PDF_Disarm')
	click.echo('Enable Copy & Disarm of PDF Document: {}'.format(disarm))
	if disarm == 'False':
		click.secho('Warning: Disarming Is Not Enabled. A Safe .PDF Doc will not be created', fg='red')
	else:
		click.echo('')

	if evi_path.endswith('/') == False:
		evi_path += '/'
	click.echo('Using Path: {}\n'.format(evi_path))

	title = 'Please Select A File From The List Below.\nIf There Is No Files, Try specifying a New Dir.'
	choices = []
	for file in os.listdir(evi_path):
		if file.lower().endswith('.pdf') and file.find('.disarmed') == -1:		#collect pdf files
			choices.append(file)
	choices.append('-- Specify .PDF Evidance Directory')
	choices.append('[0] Back')

	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		MainMenu_Controller.main_menu()
	elif index_selection == len(choices) - 2:
		index_selection = tms.generate_string_menu('PDF Evidance File Location:', 1)		#get new path
		if index_selection == '0':
			PDF_main_menu()
		else:
			PDF_main_menu(index_selection)
	else:
		sel_file = choices[index_selection]

	click.secho('- --- - WARNING - --- - --- - WARNING - --- - --- - WARNING - --- -\n', fg='red', bold=True)
	click.secho('The Following Commands Will Be Executed:', bold=True)

	pdfid_comm = ccs.PDF_pdfid_command_gen(evi_path, disarm, sel_file)			#generate commands
	click.echo(pdfid_comm + '\n')
	pdfparser_objs_comm = ccs.PDF_pdfparser_objs_command_gen(evi_path, sel_file)
	click.echo(pdfparser_objs_comm + '\n')
	pdfparser_locs_comm = ccs.PDF_pdfparser_locs_command_gen(evi_path, sel_file)
	click.echo(pdfparser_locs_comm + '\n')
	if hashes == 'True':
		pdfparser_hash_comm = ccs.PDF_pdfparser_hash_command_gen(evi_path, sel_file)
		click.echo(pdfparser_hash_comm + '\n')
	else:
		pdfparser_hash_comm = ''

	title = 'You Are About To Execute The following Commandns!!!'
	index_selection = tms.generate_promt_menu(title, 2)

	if index_selection == 0:
		PDF_main_menu()
	else:
		objs_list, paths = PDF_process_pdf_data(pdfparser_objs_comm, pdfparser_locs_comm, pdfid_comm, evi_path, sel_file, hashes, pdfparser_hash_comm)		#EXECUTE
		PDF_selection(objs_list, paths)

"""
PDF selection is a page that asksthe user what objects they would like to view (all or by stream)
requires a list of objs and a list of paths for the tool output files
"""
def PDF_selection(objs_list, paths):
	os.system('clear')
	click.secho('PDF Obj Search Selection\n', fg='blue', bold=True)

	click.secho('Object Locations:', bold=True)

	hash_path = paths[0]				#paths
	locs_path = paths[1]
	objs_path = paths[2]
	dir_path = paths[3]
	pdfid_path = paths[4]

	try:
		if scs.settings_check('$PDF_Verbose_Output') == 'True':		#display pdf-parser > pdfid
			txt = open(locs_path)
			txt_lines = txt.readlines()
			txt.close()
		else:
			txt = open(pdfid_path)
			txt_lines = txt.readlines()
			txt.close()
	except:
		click.echo('ERROR READING FILES. Perhaps Execution Was Wrong?')

	for count, line in enumerate(txt_lines):
		if count > 1:
			click.echo(line.strip())

	title = '\nHow Would You Like To Search the Objs?'
	choices = ['[1] View By Stream','[2] View All','[0] Back']
	
	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		PDF_main_menu()
	elif index_selection == 0:						#get found tags
		choices_set = set({})
		for obj in objs_list:
			if obj.get_tag() != '':
				choices_set.add(obj.get_tag())
		
		choices = []
		for choice in choices_set:
			choices.append(choice)
		choices.append('[0] Back')
		
		title = '\nWhat Object Stream Would You Like To Investigate?'
		index_selection = tms.generate_menu(title, choices)

		if index_selection == len(choices) - 1:
			PDF_selection(objs_list, paths)				
		else:
			PDF_display(objs_list, paths, choices[index_selection])		#display by tag
	elif index_selection == 1:
		PDF_display(objs_list, paths, 'all')			#display all
		pass

	MainMenu_Controller.main_menu()

"""
PDF display uses a terminal_menu script to live preview a file based on the selection of the user.
The selection is the current highlighted index in the list of choices.
requires a list of objs, tool output file paths and a tag
"""
def PDF_display(objs_list, paths, tag):
	os.system('clear')
	click.secho('PDF Obj Previewer\n', fg='blue', bold=True)

	click.secho('Press Enter To Use To View its Contnet In Full')

	org_obj_list = []					#orginise list
	check = 1
	for obj in objs_list:
		for obj in objs_list:
			if obj.get_id() == check:
				org_obj_list.append(obj)
				check = check + 1

	choices = []
	title = 'Search with "/" Or [0] To Go Back Or Nav To Bottom Of The Page\n'
	if tag == 'all':								#all selected
		for obj in org_obj_list:
			choices.append('obj_{}'.format(str(obj.get_id())))
	else:
		for obj in org_obj_list:						#selected via tag
			if obj.get_tag().strip() == tag.strip():
				choices.append('obj_{}'.format(str(obj.get_id())))
	choices.append('[0] Back')		

	index_selection = tms.generate_obj_preview_menu(title, choices, objs_list, paths[3])

	if index_selection == len(choices) - 1:
		PDF_selection(objs_list, paths)
	else:
		os.system('clear')
		click.secho('PDF Obj Contnents\n', fg='blue', bold=True)

		check = 0
		for obj in org_obj_list:
			if obj.get_tag().strip() == tag.strip() or tag == 'all':	#collect ID of index_selection
					if check == index_selection:
						code = str(obj.get_id())
						break
					else:
						check = check + 1

		os.system('more -d -f ' + paths[3] + 'obj_{}.txt'.format(code))		#display obj_x.txt file for full output
		x = input ('\n\nPlease Press [Enter] To Return')
		PDF_display(objs_list, paths, tag)
			
"""
PDF process pdf data executes multiple commands and executes them while also formating & creating files for preview use
requires commands for all 4 commands, evidance path, seleted_file, a hash check, and hash command
returns a full objs_list filled with scan PDF objects and the paths of all the files
"""
def PDF_process_pdf_data(pdfparser_objs_comm, pdfparser_locs_comm, pdfid_comm, evi_path, sel_file, hashes, pdfparser_hash_comm):
	os.system('clear')
	click.secho('PROCESSING PDF FILE\n', fg='blue', bold=True)
	
	uls_filepath = scs.settings_check('$Default_UsageLog_Location')
	if uls_filepath.endswith('/') == False:
		uls_filepath += '/'
	uls_filepath += 'Pdf_Usage_Logs.txt'
	uls_content = [pdfparser_objs_comm, pdfparser_locs_comm, pdfid_comm, pdfparser_hash_comm]
	uls.log_change(uls_filepath, 'PDF_Parse_Attmept', uls_content)

	print('LOADING PDF OBJECTS... (Pdf-Parser)')
	os.system(pdfparser_objs_comm)					#comm call
	print('DONE')

	if hashes == 'True':
		print('LOADING PDF OBJECT HASHES... (Pdf-Parser)')
		os.system(pdfparser_hash_comm)				#comm call
		print('DONE')

	print('LOADING PDF OBJECT LOCATIONS...(Pdf-Parser)')
	os.system(pdfparser_locs_comm)						#comm call
	print('DONE')
	print('FORMATTING AND GENERATING FILES FOR PREVIEW...')
	objs_list, paths = pos.get_pdf_objects_list(evi_path, sel_file, hashes)		#script call
	print('DONE')
	print('LOADING PDFID SCAN...(Pdfid)')
	os.system(pdfid_comm)						#comm call
	print('DONE')

	return objs_list, paths
