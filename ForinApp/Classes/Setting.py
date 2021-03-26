#Settings Class

class Setting:
	section = ''			#what section it is under
	description = ''		#setting description
	items = ''			#setting options
	code = '';			#setting code ("$call:var")

	def __init__(self, setting_sect, setting_desc, setting_items, setting_code):
		self.section = setting_sect
		self.description = setting_desc
		self.items = setting_items
		self.code = setting_code

	#Gets && Sets
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

	def get_code(self):
		return self.code

	def set_code(self, setting_code):
		self.code = setting_code
