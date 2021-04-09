#Pdf Object Script Test File

import pytest

from Model.PdfObject import *
from Scripts import PdfObjectsScript as pos

def test_get_DC_settings_txt():
	path = '/home/kali/Raspberry-Pi4-Forensics/ForinApp/Tests/test_dependencies/'
	filename = 'test.pdf'

	obj_list, paths = pos.get_pdf_objects_list(path, filename, 'False')

	assert len(obj_list) == 0
	assert paths[0].endswith('Tests/test_dependencies/test_parser_md5.txt') == True
	assert paths[1].endswith('Tests/test_dependencies/test_parser_locs.txt') == True
	assert paths[2].endswith('test_dependencies/test_parser_objs.txt') == True
	assert paths[3].endswith('Tests/test_dependencies/test_parser_objs/') == True
	assert paths[4].endswith('Tests/test_dependencies/test_pdfid.txt') == True
