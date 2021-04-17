#Python PDF Controller (PDF analysis)
#Application Name: Forin
#Author: J.Male
#Desc: 
#	Handles all of the operations within the application realting to PDF analysis
#	uses Tools pdf-parser and pdfid to identify pf files

import click
import sys
import os

from View import MainMenu_Controller
from Model.PdfObject import PdfObject
from Scripts import SettingsCheckScript as scs 
from Scripts import TerminalMenuScript as tms
from Scripts import UsageLoggingScript as uls
from Scripts import PdfObjectsScript as pos

"""
PDF Main Menu, Acts as the PDF file selection Page / Main Menu Page For PDF analysis
Asks the User to Select A PDF File where 3/4 Commands Are excuted to generate PDF data
requires a path that can be empty.
"""
def PDF_main_menu(path = '0'):
	if path and path != '0':
		evi_path = path
		if evi_path.endswith('/') == False:
			evi_path = evi_path + '/'
	else:
		evi_path = scs.settings_check('$Default_Output_Location')
		if evi_path.endswith('/') == False:
			evi_path = evi_path + '/'

	hashes = scs.settings_check('$PDF_Hashes')
	disarm = scs.settings_check('$PDF_Disarm')

	### Select PDF File
	os.system('clear')
	click.secho('PDF File Analysis\n', fg='blue', bold=True)
	click.echo('Pdfid and pdf-parser will scan a pdf file and Forin will display its output')
	click.echo('This Will Create A Disarmed PDF Copy, a .txt file containing the PDF objects & a txt of object locations')
	click.echo('these files can be found in the same dir as the PDF evidance.\n')
	click.echo('Note: In Order For Forin To Display Information, Txt Files Will be created FOR EACH OBJ in the pdf')
	click.echo('      This Can Have An Effect On Process Time With Larger PDF Files.\n')
	click.echo('Enable Object MD5 Hashes: {}'.format(hashes))
	click.echo('Enable Copy & Disarm of PDF Document: {}'.format(disarm))
	if disarm == 'False':
		click.secho('Warning: Disarming Is Not Enabled. A Safe .PDF Doc will not be created', fg='red')
	else:
		click.echo('')
	click.echo('Using Path: {}\n'.format(evi_path))

	title = 'Please Select A File From The List Below.\nIf There Is No Files, Try specifying a New Dir.'
	choices = []
	for file in os.listdir(evi_path):
		if file.lower().endswith('.pdf') and file.find('.disarmed') == -1:		
			choices.append(file)
	choices.append('-- Specify .PDF Evidance Directory')
	choices.append('[0] Back')

	index_selection = tms.generate_menu(title, choices)

	if index_selection == len(choices) - 1:
		MainMenu_Controller.main_menu()
	elif index_selection == len(choices) - 2:
		index_selection = tms.generate_string_menu('PDF Evidance File Location:', 1)		
		if index_selection == '0':
			PDF_main_menu()
		else:
			PDF_main_menu(index_selection)
	else:
		sel_file = choices[index_selection]

	click.secho('- --- - WARNING - --- - --- - WARNING - --- - --- - WARNING - --- -\n', fg='red', bold=True)
	click.secho('The Following Commands Will Be Executed:', bold=True)

	new_sel_file = sel_file.split('.')

	### Generate PDF-Parser / PDFID Commmands
	pdfid_comm = 'sudo pdfid '
	if disarm == 'True':
		pdfid_comm += '-d '
	txt = open(evi_path + new_sel_file[0] + '_pdfid.txt', 'w')
	txt.write('')
	txt.close()
	pdfid_comm += evi_path + sel_file + ' -o ' + evi_path + new_sel_file[0] + '_pdfid.txt'

	pdfparser_objs_comm = 'sudo pdf-parser -c -O ' + evi_path + sel_file
	pdfparser_objs_comm += ' > ' + evi_path + new_sel_file[0] + '_parser_objs.txt'
	
	pdfparser_locs_comm = 'sudo pdf-parser -a -O ' + evi_path + sel_file
	pdfparser_locs_comm += ' > ' + evi_path + new_sel_file[0] + '_parser_locs.txt'

	click.echo(pdfid_comm + '\n')
	click.echo(pdfparser_objs_comm + '\n')
	click.echo(pdfparser_locs_comm + '\n')

	if hashes == 'True':
		pdfparser_hash_comm = 'sudo pdf-parser -H ' + evi_path + sel_file
		pdfparser_hash_comm += ' > ' + evi_path + new_sel_file[0] + '_parser_md5.txt'
		click.echo(pdfparser_hash_comm + '\n')
	else:
		pdfparser_hash_comm = ''

	title = 'You Are About To Execute The following Commands!'
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
	hash_path = paths[0]
	locs_path = paths[1]
	objs_path = paths[2]
	dir_path = paths[3]
	pdfid_path = paths[4]

	os.system('clear')
	click.secho('PDF Obj Search Selection\n', fg='blue', bold=True)
	click.secho('Object Locations:', bold=True)

	### Display Type of Print Output
	try:
		if scs.settings_check('$PDF_Verbose_Output') == 'True':
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

	### Select Object Search Filter
	if index_selection == len(choices) - 1:
		PDF_main_menu()
	elif index_selection == 0:
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
			PDF_display(objs_list, paths, choices[index_selection])
	elif index_selection == 1:
		PDF_display(objs_list, paths, 'all')
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

	### Orginise PDF Objects List
	org_obj_list = []
	check = 1
	for obj in objs_list:
		for obj in objs_list:
			if obj.get_id() == check:
				org_obj_list.append(obj)
				check = check + 1
	
	### Select PDF Via 'all' or 'tag'
	choices = []
	title = 'Search with "/" Or [0] To Go Back Or Nav To Bottom Of The Page\n'
	if tag == 'all':								
		for obj in org_obj_list:
			choices.append('obj_{}'.format(str(obj.get_id())))
	else:
		for obj in org_obj_list:						
			if obj.get_tag().strip() == tag.strip():
				choices.append('obj_{}'.format(str(obj.get_id())))
	choices.append('[0] Back')		

	index_selection = tms.generate_obj_preview_menu(title, choices, objs_list, paths[3])

	### Display PDF Object Contents
	if index_selection == len(choices) - 1:
		PDF_selection(objs_list, paths)
	else:
		os.system('clear')
		click.secho('PDF Obj Contnents\n', fg='blue', bold=True)

		check = 0
		for obj in org_obj_list:
			if obj.get_tag().strip() == tag.strip() or tag == 'all':
					if check == index_selection:
						code = str(obj.get_id())
						break
					else:
						check = check + 1

		os.system('more -d -f ' + paths[3] + 'obj_{}.txt'.format(code))
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

	### Command Execution
	print('LOADING PDF OBJECTS... (Pdf-Parser)')
	os.system(pdfparser_objs_comm)					
	print('DONE')
	if hashes == 'True':
		print('LOADING PDF OBJECT HASHES... (Pdf-Parser)')
		os.system(pdfparser_hash_comm)				
		print('DONE')
	print('LOADING PDF OBJECT LOCATIONS...(Pdf-Parser)')
	os.system(pdfparser_locs_comm)						
	print('DONE')
	print('FORMATTING AND GENERATING FILES FOR PREVIEW...')
	objs_list, paths = pos.get_pdf_objects_list(evi_path, sel_file, hashes)		
	print('DONE')
	print('LOADING PDFID SCAN...(Pdfid)')
	os.system(pdfid_comm)					
	print('DONE')

	return objs_list, paths
