#Scaple Setting Class

class ScalpelSetting:
	cat = ''
	options = []			#nested list, holds a list of lists containing setting data

	def __init__(self, cat, options):
		self.cat = cat
		self.options = options
	
#Gets && Sets
	def get_cat(self):				
		return self.cat
	
	def set_cat(self, cat):
		self.cat = cat

	def get_options(self):				
		return self.options
	
	def set_options(self, options):
		self.options = options
