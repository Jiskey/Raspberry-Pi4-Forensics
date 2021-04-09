#Pdf Object class Test File

import pytest

from Model.PdfObject import *

def test_pdf_object():
	tmp = PdfObject(1, ('Headerline1','Headerline2'), ('dataline1','dataline2'), ('contentline1','contentline2'))
	tmp.set_tag('test')
	tmp.set_md5('THISISAMD5HASH')

	assert tmp.get_id() == 1
	assert tmp.get_head()[1] == 'Headerline2'
	assert tmp.get_data()[1] == 'dataline2'
	assert tmp.get_contents()[1] == 'contentline2'
	assert tmp.get_tag() == 'test'
	assert tmp.get_md5() == 'THISISAMD5HASH'
