#Python PDFObject Class
#Application Name: Forin
#Author: J.Male
#Desc: 
#	PDF Object Class Is USed To Store PDF File Parsed Data

"""
PDF Object Class Scans the objects Created By Pdf-Parser And Stores What is Belived To Be It Contents
Can Store Its MD5 If Required
"""
class PdfObject:
	obj_id = 0
	obj_head = []
	obj_data = []
	obj_contents = []
	tag = ''
	md5 = ''
	
	def __init__(self, obj_id, obj_head, obj_data, obj_contents):
		self.obj_id = obj_id
		self.obj_head = obj_head
		self.obj_data = obj_data
		self.obj_contents = obj_contents

	def get_id(self):			
		return self.obj_id

	def get_head(self):			
		return self.obj_head

	def get_data(self):			
		return self.obj_data
	
	def get_contents(self):				
		return self.obj_contents

	def get_tag(self):				
		return self.tag

	def set_tag(self, tag):				
		self.tag = tag

	def get_md5(self):				
		return self.md5

	def set_md5(self, md5):				
		self.md5 = md5
