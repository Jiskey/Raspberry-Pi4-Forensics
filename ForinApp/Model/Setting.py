#Python Setting Class
#Application Name: Forin
#Author: J.Male
#Desc: 
#	Setting Class Is the Class That holds settings collect from thew Forin App Conf File.

"""
Class Setting Holds data that is collected from the settings.txt / Config File.
Can Either Hold The Whole List Of Settings Or Just One Section Based On Settings.get_section()
"""
class Setting:
	section = ''
	description = ''		
	items = ''			
	code = '';

	def __init__(self, setting_sect, setting_desc, setting_items, setting_code):
		self.section = setting_sect
		self.description = setting_desc
		self.items = setting_items
		self.code = setting_code

	def get_section(self):
		return self.section

	def set_section(self, setting_sect):
		self.section = setting_sect

	def get_description(self):
		return self.description

	def set_description(self, setting_desc):
		self.description = setting_desc

	def get_items(self):
		return self.items

	def set_items(self, setting_items):
		self.items = setting_items

	### Setting Code str(Call:Var)
	def get_code(self):
		return self.code

	### Setting Code str(Call:Var)
	def set_code(self, setting_code):
		self.code = setting_code

	### Get Setting Call [Call:Var]
	def get_code_call(self):
		call, var = self.code.split(':')	
		return call

	### Get Setting Var [Call:Var]
	def get_code_var(self):	
		call, var = self.code.split(':')
		return var

	### Return a list of Options (list('opt1','opt2',...))
	def get_items_list(self):
		list_items = self.items[1:-1]
		list_items = list_items.split('][')	
		return list_items
