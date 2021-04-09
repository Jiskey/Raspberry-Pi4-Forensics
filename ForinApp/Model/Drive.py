#Drive Class

class Drive:
	path = ''						
	size = 0
	size_bytes = 0
	sectors = 0
	model = ''
	sector_size = ''
	disklabel = ''
	identifier = ''
	boot = False
	partitions = [];

	def __init__(self, path, size, size_bytes, sectors, model, sector_size, disklabel, identifier, boot, partitions):
		self.path = path						
		self.size = size
		self.size_bytes = size_bytes
		self.sectors = sectors
		self.model = model
		self.sector_size = sector_size
		self.disklabel = disklabel 
		self.identifier = identifier 
		self.boot = boot
		self.partitions = partitions

#Gets (Will Never Set)
	def get_path(self):				#path
		return self.path

	def get_size(self):				#size (GB)
		return self.size

	def get_size_bytes(self):			#size (bytes)
		return self.size_bytes
	
	def get_sectors(self):				#sectors
		return self.sectors

	def get_model(self):				#model
		return self.model

	def get_sector_size(self):			#sector size (log/phys)
		return self.sector_size

	def get_disklabel(self):			#label	
		return self.disklabel

	def get_identifier(self):			#indetifaction code
		return self.identifier

	def get_boot(self):				#boot	
		return self.boot

	def get_partitions(self):			#partitions
		return self.partitions

	def get_partition(self, part):
		return self.partitions[part]
	
#Data Format Functions
	def get_partition_path(self, part):				#get partition path
		part_path, part_start, part_end, part_type = self.partitions[part].split(':')
		return part_path
	
	def get_partition_start(self, part):				#get partition sectors start
		part_path, part_start, part_end, part_type = self.partitions[part].split(':')
		return int(part_start)

	def get_partition_end(self, part):				#get partition sectors end
		part_path, part_start, part_end, part_type = self.partitions[part].split(':')
		return int(part_end)

	def get_partition_sectors(self, part):				#get partition sectors
		part_path, part_start, part_end, part_type = self.partitions[part].split(':')
		part_sectors = (int(part_end) - int(part_start)) + 1
		return int(part_sectors)

	def get_partition_size(self, part):				#get partition sectors size (GB)
		part_path, part_start, part_end, part_type = self.partitions[part].split(':')
		part_sectors = (int(part_end) - int(part_start)) + 1
		part_sectors = part_sectors * 512
		part_sectors = part_sectors / 1024
		part_sectors = part_sectors / 1024
		part_sectors = part_sectors / 1024
		return float(part_sectors)

	def get_partition_size_bytes(self, part):    			#get partition sectors size (bytes)
		part_path, part_start, part_end, part_type = self.partitions[part].split(':')
		part_sectors = (int(part_end) - int(part_start)) + 1
		part_sectors = part_sectors * 512
		return int(part_sectors)

	def get_partition_type(self, part):				#get partition type
		part_path, part_start, part_end, part_type = self.partitions[part].split(':')
		return part_type

	def get_sector_size_log(self):					#get logical sector size
		log, pyhs = self.sector_size.split(':')
		return int(log)

	def get_sector_size_pyhs(self):					#get physical sector size
		log, pyhs = self.sector_size.split(':')
		return int(pyhs)


