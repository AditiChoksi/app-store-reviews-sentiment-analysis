class Merge():

	def __init__(self,path, file_num):
		self.path = path
		self.file_num = file_num
		self.file1 = self.file_num+'.csv'
		self.file2 = self.file_num+'_scores.csv'
	
	def merge(self):
		reader1 = open(self.path + self.file1, 'r')
		reader2 = open(self.path + self.file2, 'r')

		writer = open(self.path + self.file_num+'_merged.csv', 'w')
				
		for line in reader1:
			line2 = reader2.readline()
			to_write = line.strip() + ',' + line2
			writer.write(to_write)


for curr in range(8,208):
	merger = Merge('/home/ash/workspace/mehul/dmw_project/flask-app/review_filtered/',str(curr))
	merger.merge()
					
