#Python DcObject Model (Data Carving)
#Application Name: Forin
#Author: J.Male
#Desc: 
#	DcObject Is a Simple Class that Holdsa Category Name And a List Of Extensions
#	exts(ext(tag, extension, y/n, size, header, ...)) (Nested List)

class DcObject:
	cat = ''
	exts = []

	def __init__(self, cat, exts):
		self.cat = cat
		self.exts = exts

	def get_cat(self):					# Object Category		
		return self.cat
	
	def set_cat(self, cat):
		self.cat = cat

	def get_exts(self):					# List Of Extentions
		return self.exts
	
	def set_exts(self, objects):
		self.exts = exts
