#pdf Object Class

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

#Gets && Sets
	def get_id(self):				#int id
		return self.obj_id

	def get_head(self):				#obj_head list contains file lines
		return self.obj_head

	def get_data(self):			#list contains file lines
		return self.obj_data
	
	def get_contents(self):				#list contains file lines
		return self.obj_contents

	def get_tag(self):				#get the set pdf-parser tag
		return self.tag

	def set_tag(self, tag):				#get the set pdf-parser tag
		self.tag = tag

	def get_md5(self):				#md5 hash == '' if Error
		return self.md5

	def set_md5(self, md5):				
		self.md5 = md5
