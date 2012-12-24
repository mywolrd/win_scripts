import os, shutil

class Mine:
				
	def moveFiles(self):
		if os.path.isdir(self.cwd):
			path = self.cwd+"\\"
			dirList = [ path+d for d in os.listdir(path)]
			
			for dir in dirList:
				newDir = dir + "\\"
				print newDir
				#fileList = [ newDir + f for f in os.listdir(newDir)]
				
				#for file in fileList:
				#	shutil.copy(file, path)
				
				#shutil.rmtree(newDir)
	
	def __init__(self):
		self.cwd = os.getcwd()
		self.moveFiles()	
		
Mine()		