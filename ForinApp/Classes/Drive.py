class Drive:
	number = 0
	path = ""
	size_gb = 0
	size_bytes = 0;

	def __init__(self, drive_number, drive_path, drive_size_gb, drive_size_bytes):
		self.number = drive_number
		self.path = drive_path
		self.size_gb = drive_size_gb
		self.size_bytes = drive_size_bytes
		
		self.drive_partitions = []
		self.partition_selection = ''

	#Gets && Sets
	def get_number(self):
		return self.number

	def set_number(self, drive_number):
		self.number = drive_number

	def get_path(self):
		return self.path

	def set_path(self, path_name):
		self.path = path_name

	def get_size_gb(self):
		return self.size_gb

	def set_size_gb(self, drive_size_gb):
		self.size_gb = drive_size_gb

	def get_size_bytes(self):
		return self.size_bytes

	def set_size_bytes(self, drive_size_bytes):
		self.size_bytes = drive_size_bytes

	def get_partition_selection(self):
		return self.partition_selection

	def set_partition_selection(self, partition_selection):
		self.partition_selection = partition_selection

	def get_partitions(self):
		return self.drive_partitions

	def get_drive_partition(self, section):
		return self.drive_partitions[section]

	def add_drive_partition(self, section):
		self.drive_partitions.append(section)

	def del_drive_partition(self, section):
		self.drive_partitions.remove(section)
